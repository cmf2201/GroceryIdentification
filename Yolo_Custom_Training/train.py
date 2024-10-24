from ultralytics import YOLO

def main():
    config_path = r'datasets/config.yaml' # change to your dataset config path

    # Load a model
    model = YOLO('yolo11n.pt')
    # Set the device to CPU
    model.to('cuda')
    # Use the model with a reduced batch size
    # model.train(data=config_path, epochs=200, batch=16, amp=False)
    model.train(data="SKU-110K.yaml", epochs=100, imgsz=640)
if __name__ == '__main__':
    main()