from roboflow import Roboflow
rf = Roboflow(api_key="dzMZR2CqtSEaV7uZ7cV6") # Your API key here. Current is from groceryassistant/grocery-shopping-images/1/
project = rf.workspace("groceryassistant").project("grocery-shopping-images") # Your project here
version = project.version(1)
dataset = version.download("yolov11")
                