import kagglehub

# Download latest version
path = kagglehub.dataset_download("kvnpatel/fruits-vegetable-detection-for-yolov4")

print("Path to dataset files:", path)