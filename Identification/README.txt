Setting up identification:
conda enviornment required
currently runs/detect/train has weights for a trained dataset on https://github.com/aleksandar-aleksandrov/groceries-object-detection-dataset
yolov10n.pt is the pretrained nano yolov10 model found here: https://docs.ultralytics.com/models/yolov10/

1. install github dependencies
cd identification
git clone https://github.com/THU-MIG/yolov10.git
git clone https://github.com/PD-Mera/yolo-data-visualization.git

2. upgrade pip if needed:
python.exe -m pip install --upgrade pip

3. Install ultralytics:
pip install ultralytics

4. Install YOLOv10 dependencies:
cd ./yolov10
pip install .

5. make sure ultralytics is at ultralytics-8.3.2
pip show ultralytics
pip install ultralytics --upgrade

6. install pylabel if you are converting datasets
pip install pylabel


for training a custom model:
