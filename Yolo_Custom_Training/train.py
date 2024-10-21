import os
from ultralytics import YOLO

def main():
    config_path = r'datasets/config.yaml'

    # Load a model
    model = YOLO('yolo11n.pt')
    # Use the model with a reduced batch size
    model.train(data=config_path, epochs=200, batch=16, amp=False) # modify params for different training

if __name__ == '__main__':
    main()