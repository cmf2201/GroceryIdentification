Setting up identification:
1. upgrade pip if needed:
python.exe -m pip install --upgrade pip

2. Install ultralytics:
pip install ultralytics

3. Install YOLOv10 dependencies:
cd ./yolov10
pip install .

4. make sure ultralytics is at ultralytics-8.3.2
pip show ultralytics
pip install ultralytics --upgrade

5. install pylabel if you are converting datasets
pip install pylabel