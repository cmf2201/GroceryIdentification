import torch
"""
This script checks if CUDA is available for PyTorch and provides information about the GPU.
1. Prints the version of PyTorch being used.
2. Checks if CUDA is available.
3. If CUDA is available, it prints the current CUDA device and the name of the GPU.
"""

# RUN THIS FILE TO CHECK IF WHEN TRAINING IT WILL USE CUDA OR NOT

print("Torch version:", torch.__version__)
print("Is CUDA available?", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Current device:", torch.cuda.current_device())
    print("Device name:", torch.cuda.get_device_name(0))
