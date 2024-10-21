Setting up training and identifcation testing:
conda enviornment required
currently runs/detect/train has weights for a trained dataset on https://github.com/aleksandar-aleksandrov/groceries-object-detection-dataset
YOLOv11 will automatically download whatever model you want in real_time_yolo_demo.py

1. install github dependencies for visualizing data if needed
cd identification
git clone https://github.com/PD-Mera/yolo-data-visualization.git

2. upgrade pip if needed:
python.exe -m pip install --upgrade pip

3. Install ultralytics:
pip install ultralytics

4. install pylabel if you are converting datasets
pip install pylabel

5. make sure ultralytics is at ultralytics-8.3.2
pip show ultralytics
pip install ultralytics --upgrade