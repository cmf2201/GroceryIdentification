import os
from ultralytics import YOLO

def main():
    # modify for your datasets data.yaml path
    config_path = r'datasets/YOUR_DATASET_PATH/data.yaml'
    # Load a model
    model = YOLO('yolo11s.pt')
    # Use the model with a reduced batch size
    model.train(data=config_path, epochs=100, batch=16, amp=False, project='./runs') # modify params for different training

if __name__ == '__main__':
    main()