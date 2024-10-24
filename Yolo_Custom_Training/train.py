from ultralytics import YOLO

def main():
    config_path = r'datasets/config.yaml' # change to your dataset config path

    # Load a model
    model = YOLO('yolo11n.pt', device='cuda')
    # Use the model with a reduced batch size
    model.train(data=config_path, epochs=200, batch=16, amp=False)

if __name__ == '__main__':
    main()