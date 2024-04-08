from flask import Flask,jsonify,request
import torch
import torch_pruning as tp
import torch.nn as nn
import compress
import database
from flask_cors import CORS
import subprocess
import base64,json
from compress import compress_pth_file

from torchvision.models import (
    resnet50, 
    densenet121,
    mobilenet_v2,
    googlenet,
    inception_v3,
    squeezenet1_1,
    vgg16_bn,
    vgg19_bn,
    mnasnet1_0,
    alexnet,
    convnext_base,
    efficientnet_b0,
    resnet101,
    resnet152,
    resnet18,
    resnet34,
    densenet161,
    mnasnet0_5,
    regnet_x_16gf,
    vgg11,
)

app = Flask(__name__)
CORS(app)
model_mapping= {
        "resnet18": resnet18,
        "resnet50": resnet50,
        "densenet121": densenet121,
        "mobilenet_v2": mobilenet_v2,
        "alexnet": alexnet,
        "googlenet":googlenet,
        "inception_v3":inception_v3,
        "squeezenet1_1":squeezenet1_1,
        "vgg16_bn":vgg16_bn,
        "vgg19_bn":vgg19_bn,
        "mnasnet1_0":mnasnet1_0,
        "convnext_base":convnext_base,
        "efficientnet_b0":efficientnet_b0,
        "resnet101":resnet101,
        "resnet152":resnet152,
        "resnet34":resnet34,
        "densenet161":densenet161,
        "mnasnet0_5":mnasnet0_5,
        "regnet_x_16gf":regnet_x_16gf,
        "vgg11":vgg11,
    }


@app.route("/")
def test():
    model = resnet18(pretrained=True).eval()
    return str(model)


@app.route("/compress", methods=['POST'])
def compress():
    global progress_value, accuracy, params, ops
    progress_value = -1
    accuracy = []
    params = []
    ops = []

    post_data = request.json  # 假设 request 是你的请求对象
    print(str(request.data))
    print(str(post_data))

    model_info = post_data.get("model_info", {})
    train_info = post_data.get("train_info", {})

    # 从 model_info 中获取各个字段的值
    dataset = model_info.get("dataset")
    method = model_info.get("method")
    is_default = model_info.get("isDefault")
    model_type = model_info.get("model_type")
    example_input = model_info.get("example_input")
    ratio = model_info.get("ratio")
    save_location = model_info.get("save_location")
    model_params = model_info.get("model_params")
    if_fine_tuning = model_info.get("ifFineTuning")

    # 从 train_info 中获取各个字段的值
    epochs = train_info.get("epochs")
    lr = train_info.get("lr")
    print_freq = train_info.get("print_freq")
    batch_size = train_info.get("batch_size")
    
    if dataset=="ImageNet":
    # 输出 POST 请求的参数
        command = ['python', 'Pruning/Torch-Pruning/benchmarks/main_imagenet.py',
            '--prune',
            '--pretrained']

        command.extend(['--output-dir', "compressed_models"])
        command.extend(['--data-path', "Pruning/Torch-Pruning/benchmarks/data/torchdata/ImageNet/val"])

        if model_type:
            command.extend(['--model', model_type])
        if method:
            command.extend(['--method', method])
        # if example_input:
        #     command.extend(['--batch-size', str(example_input[0])])  # Convert to string
        if ratio:
            command.extend(['--target-flops', str(ratio/100.0)])  # Convert to string

        if epochs:
            command.extend(['--epochs', str(epochs)])
        if lr:
            command.extend(["--lr", str(lr)])
        if print_freq:
            command.extend(["--print-freq", str(print_freq)])
        if batch_size:
            command.extend(["--batch-size", str(batch_size)])
    # else:
    #     command = ['python', 'Pruning/Torch-Pruning/benchmarks/main.py']

    #     command.extend(['--mode', 'prune'])
    #     if dataset:
    #         command.extend(['--dataset', str(dataset)])

    print(str(command))
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 循环读取子进程的输出
    while process.poll() is None:
        output = process.stdout.readline().decode().strip()
        # 解析输出，提取进度信息
        print(output)
        if "progress" in output:
            progress_str = output.split(":")[1].strip()  # 提取冒号后面的值，并去除首尾空格
            progress_value = float(progress_str)  # 将字符串转换为浮点数
            # print(progress_value)
        if "accuracy" in output:
            accuracy_str = output.split(":")[1].strip()
            accuracy.append(float(accuracy_str))
        if "parameters" in output:
            params_str = output.split(":")[1].strip()
            params.append(float(params_str))
        if "operations" in output:
            ops_str = output.split(":")[1].strip()
            ops.append(float(ops_str))

    # 等待子进程结束
    process.wait()
    torch.cuda.empty_cache()
    
    # 压缩 .pth 文件
    pth_file_path = 'compressed_models/best.pth'
    gzip_file_path = 'compressed_models/best_compressed.pth'

    compress_pth_file(pth_file_path, gzip_file_path)

    with open(gzip_file_path, 'rb') as file:
        compressed_model_bytes = file.read()

    compressed_model = base64.b64encode(compressed_model_bytes).decode('utf-8')


    # 返回二进制数据和其他元数据
    data = {
        "id": 1234,
        "model":compressed_model,
        "compression_method": "gzip"
    }
    return jsonify(data)


@app.route("/progress", methods=['GET'])
def progress():
    # print(progress_value)
    data = {
        "progress":progress_value,
        "cur_accuracy":accuracy
    }
    return jsonify(data)


@app.route("/analysis", methods=['GET'])
def analysis():
    #读出文件内容，accuracy, params, ops
    data = {
        "accuracy":accuracy,
        "params":params,
        "ops":ops
    }
    return jsonify(data)

