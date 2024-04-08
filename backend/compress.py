import torch
from torchvision.models import resnet18
import torch_pruning as tp
import gzip
import base64

def model_compress(model):
    # 获取剪枝后的状态字典
    state_dict = tp.state_dict(model)

    # 将剪枝后的状态字典保存到本地的.pth文件中
    torch.save(state_dict, 'pruned_model.pth')

    # 读取本地的.pth文件并进行压缩
    with open('pruned_model.pth', 'rb') as f:
        compressed_data = gzip.compress(f.read())
    

    compressed_data_base64 = base64.b64encode(compressed_data).decode('utf-8')

    # 返回 base64 编码的字符串
    return compressed_data_base64



def compress_pth_file(pth_file_path, gzip_file_path):
    with open(pth_file_path, 'rb') as f_in:
        with gzip.open(gzip_file_path, 'wb') as f_out:
            f_out.writelines(f_in)
