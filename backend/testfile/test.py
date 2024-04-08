import torch

checkpoint = torch.load("model (1).pth", map_location=torch.device('cuda'))
# model = checkpoint['model']
checkpoint_keys = checkpoint.keys()
checkpoint_keys_list = list(checkpoint_keys)
print(checkpoint_keys_list)
print(checkpoint['model'])

    # # model.load_state_dict(checkpoint['model'].state_dict())
    # # print(checkpoint['model'].state_dict().keys())
    