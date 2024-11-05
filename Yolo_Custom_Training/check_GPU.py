import torch

# RUN THIS FILE TO CHECK IF WHEN TRAINING IT WILL USE CUDA OR NOT

print("Torch version:", torch.__version__)
print("Is CUDA available?", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Current device:", torch.cuda.current_device())
    print("Device name:", torch.cuda.get_device_name(0))