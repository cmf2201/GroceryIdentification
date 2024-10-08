import os
from ultralytics import YOLO

def main():
    config_path = r'datasets/config.yaml'

    # Load a model
    model = YOLO("yolov10n.pt")
    # Use the model with a reduced batch size
    model.train(data=config_path, epochs=100, batch=16, amp=False)

if __name__ == '__main__':
    main()