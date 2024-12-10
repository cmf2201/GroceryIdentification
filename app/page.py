from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
import os
import sys
import json
from shapely.geometry import Polygon, Point
# Add the directory containing raycasting.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from raycasting import is_point_inside_polygon
from list_manager.list_manager import ListManager
class Page(QWidget):
    def __init__(self):
        super(Page, self).__init__()
        self.listManager = ListManager([0,0,0,0,0])
        self.initialize()
    
    def initialize(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("""background-color: #A7DCA5;""")
        layout.setContentsMargins(1,1,1,1)

        self.pageController = QStackedWidget(self)

        homepage = HomePage(self)
        newlistpage = ShoppingListPage(self)
        shoppage = ShopPage(self)

        self.pageController.addWidget(homepage)
        self.pageController.addWidget(newlistpage)
        self.pageController.addWidget(shoppage)

        self.changePage(0)
        layout.addWidget(self.pageController)
        self.setLayout(layout)

    def changePage(self, index):
        self.pageController.setCurrentIndex(index)

    def clearLayout(self):
        self.deleteLater(self.layout())

    def getList(self):
        return self.listManager

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.initialize()
    
    def initialize(self):
        if self.layout() is not None:
            self.parent.clearLayout()

        self.setStyleSheet("""background-color: #A7DCA5;""")
        outerLayout = QVBoxLayout()
        outerLayout.setContentsMargins(0,0,0,0)

        header = QVBoxLayout()
        header.setContentsMargins(10,10,10,10)
        header.setAlignment(Qt.AlignmentFlag.AlignTop)

        content = QVBoxLayout()
        content.setContentsMargins(10,10,10,10)
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)

        picture = QLabel()
        picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pictureMap = QPixmap("app/images/Groceries.PNG")
        picture.setPixmap(pictureMap)
        picture.setScaledContents
        picture.setMaximumSize(360,360)
        header.addWidget(picture)

        pageHeader = QLabel("Grocery Assistant")
        pageHeader.setFont(QFont("Georgia", 28))
        pageHeader.setMaximumHeight(100)
        pageHeader.setContentsMargins(0,10,0,0)
        pageHeader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(pageHeader)
        outerLayout.addLayout(header)

        newListBtn = QPushButton("New Shopping List", self)
        if self.parent.getList().shopping_list.items():
            newListBtn.setText("View Shopping List")
        newListBtn.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                color: black;
                border: 2px solid #90CF8E;
                border-radius: 14px;
                padding: 10px 20px;              
                font: 20pt 'Georgia'
                }
                                """)
        newListBtn.setMaximumSize(360, 100)
        newListBtn.clicked.connect(self.goToNewListPage)
        content.addWidget(newListBtn)

        shopBtn = QPushButton("Shop", self)
        shopBtn.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                color: black;
                border: 2px solid #90CF8E;
                border-radius: 14px;
                padding: 10px 20px;              
                font: 20pt 'Georgia'
                }
                                """)
        shopBtn.setMaximumSize(360, 100)
        shopBtn.clicked.connect(self.goToShopPage)
        content.addWidget(shopBtn)

        outerLayout.addLayout(content)
        self.setLayout(outerLayout)

    def goToNewListPage(self):
        self.parent.changePage(1)

    def goToShopPage(self):
        self.parent.changePage(2)

class ShopPage(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.manageList = parent.getList()
        self.use_webcam = True  # Default to using the webcam
        self.initialize()
    
    def initialize(self):
        self.setStyleSheet("""background-color: #A7DCA5;""")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Create a widget to hold the webcam feed and set its size policy
        self.webcamLabel = QLabel(self)
        self.webcamLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.webcamLabel.setFixedHeight(int(self.height() * 0.8))  # Set height to 80% of the screen
        layout.addWidget(self.webcamLabel)

        # Create a widget to hold the shopping list and cart items
        listWidget = QWidget(self)
        listLayout = QVBoxLayout(listWidget)
        listLayout.setContentsMargins(0, 0, 0, 0)

        listLabel = QLabel("Shopping List")
        listLabel.setFont(QFont("Georgia", 20))
        listLayout.addWidget(listLabel)

        self.shoppingListContents = QVBoxLayout()
        listLayout.addLayout(self.shoppingListContents)

        cartLabel = QLabel("Items in Cart")
        cartLabel.setFont(QFont("Georgia", 20))
        listLayout.addWidget(cartLabel)

        self.cartContents = QVBoxLayout()
        listLayout.addLayout(self.cartContents)

        layout.addWidget(listWidget)

        setupBtn = QPushButton("Setup", self)
        setupBtn.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                color: black;
                border: 2px solid #90CF8E;
                border-radius: 14px;
                padding: 5px 10px;              
                font: 12pt 'Georgia'
                }
                                """)
        setupBtn.setMaximumSize(180, 50)
        setupBtn.clicked.connect(self.captureAndSetup)
        layout.addWidget(setupBtn, alignment=Qt.AlignmentFlag.AlignBottom)

        switchBtn = QPushButton("Switch to Video", self)
        switchBtn.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                color: black;
                border: 2px solid #90CF8E;
                border-radius: 14px;
                padding: 5px 10px;              
                font: 12pt 'Georgia'
                }
                                """)
        switchBtn.setMaximumSize(180, 50)
        switchBtn.clicked.connect(self.switchSource)
        layout.addWidget(switchBtn, alignment=Qt.AlignmentFlag.AlignBottom)

        backBtn = QPushButton("Back", self)
        backBtn.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                color: black;
                border: 2px solid #90CF8E;
                border-radius: 14px;
                padding: 5px 10px;              
                font: 12pt 'Georgia'
                }
                                """)
        backBtn.setMaximumSize(180, 50)
        backBtn.clicked.connect(self.goBack)
        layout.addWidget(backBtn, alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(layout)
        self.startWebcam()

    def startWebcam(self):
        if self.use_webcam:
            self.capture = cv2.VideoCapture(0)  # Use the actual webcam
        else:
            video_path = "C:\\Users\\bmanw\\GroceryIdentification\\yolo_custom_training\\example_video_shor.mp4"
            self.capture = cv2.VideoCapture(video_path)  # Use the video file

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(20)

        # Load polygons from polygons.json
        try:
            with open('polygons.json', 'r') as f:
                content = f.read().strip()
                if content:
                    self.polygons = json.loads(content)
                    print("Polygons loaded from polygons.json")
                else:
                    print("polygons.json is empty, starting with empty polygons")
                    self.polygons = {'cart': []}
        except (FileNotFoundError, json.JSONDecodeError):
            print("polygons.json not found or invalid, starting with empty polygons")
            self.polygons = {'cart': []}

        # Load the YOLO model
        model_path = 'yolo11s.pt'
        self.model = YOLO(model_path, verbose=True)
        self.TRACKED_CLASSES = [46, 47, 48, 49, 50, 52, 53, 54, 55, 56]
        self.track_history = defaultdict(lambda: [])
        self.last_seen = {}
        self.max_frames_missing = 30  # Number of frames to wait before removing a track
        self.current_tracks = []
        self.frame_count = 0

    def switchSource(self):
        self.use_webcam = not self.use_webcam
        self.capture.release()
        self.startWebcam()

    def updateFrame(self):
        class_names = {
            46: 'bananas',
            47: 'apples',
            48: 'carrots',
            49: 'oranges',
            50: 'broccoli',
            52: 'pizza',
            53: 'hot dog',
            54: 'sandwich',
            55: 'cake',
            56: 'donut'  # Add the missing class ID
        }
        ret, frame = self.capture.read()
        if ret:
            # Run YOLO tracking on the full-resolution frame
            results = self.model.track(frame, persist=True, classes=self.TRACKED_CLASSES, tracker="bytetrack.yaml", conf=0.35)
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id
            class_ids = results[0].boxes.cls
            if track_ids is not None:
                track_ids = track_ids.int().cpu().tolist()
            else:
                track_ids = []
            if class_ids is not None:
                class_ids = class_ids.int().cpu().tolist()
            else:
                class_ids = []

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Draw polygons on the annotated frame
            for polygon in self.polygons['cart']:
                cv2.polylines(annotated_frame, [np.array(polygon, np.int32).reshape((-1, 1, 2))], isClosed=True, color=(0, 255, 0), thickness=5)

            # Plot the tracks
            for box, track_id, class_id in zip(boxes, track_ids, class_ids):
                x, y, w, h = box
                track = self.track_history[track_id]
                track.append((float(x), float(y)))  # x, y center point
                if len(track) > 30:  # retain 30 tracks for 30 frames
                    track.pop(0)

                # Calculate the bounding box center
                bbox_center = (x, y)

                # Check if the bounding box center is inside any polygon
                in_cart = False
                for polygon in self.polygons['cart']:
                    in_cart = in_cart or is_point_inside_polygon(bbox_center, polygon)

                if in_cart and (track_id not in self.current_tracks):
                    print("Adding item to cart: ", class_names[class_id])
                    self.manageList.add_item_to_cart(class_names[class_id])
                    self.refreshList()  # Refresh the list to update the cart items

                if track_id not in self.current_tracks:
                    self.current_tracks.append(track_id)

                self.last_seen[track_id] = (self.frame_count, class_id)

            # Remove tracks that have not been seen for a while
            for track_id in list(self.last_seen.keys()):
                if self.frame_count - self.last_seen[track_id][0] > self.max_frames_missing:
                    class_id = self.last_seen[track_id][1]
                    if class_id is not None:
                        print("Removing item from cart: ", class_names[class_id])
                        self.manageList.remove_item_from_cart(class_names[class_id])
                        self.refreshList()  # Refresh the list to update the cart items
                    self.current_tracks.remove(track_id)
                    del self.last_seen[track_id]

            # Resize the annotated frame for display
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            image = QImage(annotated_frame, annotated_frame.shape[1], annotated_frame.shape[0], QImage.Format.Format_RGB888)
            scaled_image = image.scaled(self.webcamLabel.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.webcamLabel.setPixmap(QPixmap.fromImage(scaled_image))

            self.frame_count += 1

    def captureAndSetup(self):
        ret, frame = self.capture.read()
        if ret:
            # Save the captured frame as an image
            image_path = "captured_image.jpg"
            cv2.imwrite(image_path, frame)  # Save the native resolution image
            # Call the setup_assistant script with the captured image
            os.system(f"python setup_assistant.py {image_path}")
            # Reload polygons after setup
            self.loadPolygons()

    def loadPolygons(self):
        # Load polygons from polygons.json
        try:
            with open('polygons.json', 'r') as f:
                content = f.read().strip()
                if content:
                    self.polygons = json.loads(content)
                    print("Polygons loaded from polygons.json")
                else:
                    print("polygons.json is empty, starting with empty polygons")
                    self.polygons = {'cart': []}
        except (FileNotFoundError, json.JSONDecodeError):
            print("polygons.json not found or invalid, starting with empty polygons")
            self.polygons = {'cart': []}

    def setup_assistant(self, image_path):
        # Implement the setup_assistant function
        print(f"Running setup_assistant on {image_path}")

    def populateList(self, layout, items):
        # Clear the existing items
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        # Populate with new items
        for item, quantity in items.items():
            itemLabel = QLabel(f"{item}: {quantity}")
            itemLabel.setFont(QFont("Georgia", 14))  # Make the font size smaller
            layout.addWidget(itemLabel)

    def refreshList(self):
        self.populateList(self.shoppingListContents, self.manageList.shopping_list)
        self.populateList(self.cartContents, self.manageList.cart_items)

    def showEvent(self, event):
        self.refreshList()
        super().showEvent(event)

    def goBack(self):
        self.parent.changePage(0)

class ShoppingListPage(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.manageList = parent.getList()
        self.initialize()
    
    def initialize(self):
        #Clear any past layout data
        if self.layout() is not None:
            self.parent.clearLayout()

        #Setup layout
        self.setStyleSheet("""background-color: #A7DCA5;""")
        self.outerLayout = QVBoxLayout()
        self.outerLayout.setContentsMargins(0,0,0,0)
        topLayer = QHBoxLayout() 
        topLayer.setContentsMargins(10,10,10,10)

        
        #Make Home navigation
        goHomeBtn = QPushButton("Home", self)
        goHomeBtn.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                color: black;
                border-radius: 8;
                font: 16pt 'Georgia';
                                }
                                """)
        goHomeBtn.setMaximumSize(80,50)
        goHomeBtn.clicked.connect(self.gotToHomePage)
        topLayer.addWidget(goHomeBtn)
        

        #Make Page header
        pageLabel = QLabel("Current List")
        pageLabel.setFont(QFont("Georgia", 28))
        pageLabel.setMaximumHeight(50)
        pageLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        topLayer.addWidget(pageLabel)
        topLayer.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.outerLayout.addLayout(topLayer)

        #Make section leader
        self.sectionHeader = QHBoxLayout()
        self.sectionHeader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #Make button/section for adding new items to the list
        self.addFoodButton = QPushButton("Add Item", self)
        self.addFoodButton.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                color: black;
                border-radius: 8;
                font: 16pt 'Georgia';
                                }
                                """)
        self.addFoodButton.setFixedSize(120,50)
        self.addFoodButton.clicked.connect(self.changeBaseLayout)
        self.sectionHeader.addWidget(self.addFoodButton)

        #Set the food button to visible
        #This will let us dynamically change whats in the section header
        #Swapping between the entry form and button
        self.addFoodButton.setVisible(True)
        self.outerLayout.addLayout(self.sectionHeader)

        #Create tab holder
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabBar::tab{ 
                background-color: #E4FDE1;
                color: black;
                border: 3px solid #FFFFFF;
                font: 16pt 'Georgia';
                width: 167px;
                padding: 2px;
                }""")
        #Add two tabs
        listTab = QWidget()
        cartTab = QWidget()

        #Make Cart Widget
        #Make Current Basket Widget
        cartContents = QScrollArea()
        cartContents.setWidgetResizable(True)
        cartContents.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        cartContents.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        #Then make container to hold cart area
        cartContainer = QWidget()

        #Create layout to hold previous container and update whats inside of the tab
        self.shoppingCartContents = QVBoxLayout()
        self.shoppingCartContents.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.shoppingCartContents.setSpacing(20)
        #Add container to the list tab
        cartContents.setWidget(cartContainer)
        
        #We have to specify the layout of the tab widget as well
        cartTabLayout = QVBoxLayout()
        cartTabLayout.setContentsMargins(0,0,0,0)
        cartTabLayout.addWidget(cartContents)
        cartTab.setLayout(cartTabLayout)

        # Make List Widget
        # Start by making scroll area containing everything
        listContents = QScrollArea()
        listContents.setWidgetResizable(True)
        listContents.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        listContents.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        #Then make container to hold scroll area
        listContainer = QWidget()

        #Create layout to hold previous container and update whats inside of the tab
        self.shoppingListContents = QVBoxLayout()
        self.shoppingListContents.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.shoppingListContents.setSpacing(20)
        #Set the container to the layout
        listContainer.setLayout(self.shoppingListContents)
        #Add container to the list tab
        listContents.setWidget(listContainer)

        #We have to specify the layout of the tab widget as well
        cartTabLayout = QVBoxLayout()
        cartTabLayout.setContentsMargins(0,0,0,0)
        cartTabLayout.addWidget(listContents)
        listTab.setLayout(cartTabLayout)
        
        #Finalize page
        tabs.addTab(listTab, "Shopping List")
        tabs.addTab(cartTab, "Shopping Cart")
        self.outerLayout.addWidget(tabs)
        self.setLayout(self.outerLayout)
        self.grabListData()
        

    #Function to swap between the button and form
    def changeBaseLayout(self):
        if self.addFoodButton.isVisible():
            self.addItem = addItem(self)
            self.addFoodButton.setVisible(False)
            self.sectionHeader.addWidget(self.addItem)
            self.sectionHeader.update()
        else: 
            self.addFoodButton.setVisible(True)
            self.addItem.deleteLater()
            self.sectionHeader.update()

    #Function to actually add the new item to the backend list
    def makeNewItem(self):
        itemName = self.addItem.getName()
        quantity = self.addItem.getQuantity()
        #Cast string input to int
        itemQuantity = int(quantity)
        #Add to parent list_manager
        self.manageList.add_item_to_list(itemName, itemQuantity)
        #Update scroll area with items
        self.grabListData()

    #Change to home page
    def gotToHomePage(self):
        self.parent.changePage(0)

    #Get the list_manager from page
    def getList(self):
        return self.manageList

    #Populate tba with current list data
    def grabListData(self):
        while self.shoppingListContents.count():
            widget = self.shoppingListContents.takeAt(0)
            if widget.widget():
                widget.widget().deleteLater()
        if self.manageList.shopping_list:
            for item, quantity in self.manageList.shopping_list.items():
                temp = BasketItem(item, quantity, parent=self)
                self.shoppingListContents.addWidget(temp)
                self.outerLayout.update()

    #Populate tab with current cart data
    def grabCartData(self):
        while self.shoppingCartContents.count():
            widget = self.shoppingCartContents.takeAt(0)
            if widget.widget():
                widget.widget().deleteLater()
        if self.manageList.cart_items:
            for item, quantity in self.manageList.cart_items.items():
                temp = CartItem(item, quantity, parent=self)
                self.shoppingCartContents.addWidget(temp)
                self.outerLayout.update()

    #Delete an item from the list (parent function)
    def deleteItem(self, name, quantity):
        self.manageList.remove_item_from_list(name, quantity)

    #Edit an item from the list (parent function)
    def editItem(self, name, quantity):
        self.manageList.modify_quantity_of_list(name, quantity)

class BasketItem(QWidget):
    """This widget is built out of a collection of other widgets
    As such we make a core layout to contain all of them, giving
    some buffer space between that and the scroll area they will
    exist within"""
    def __init__(self, itemName:str, quantity:int, itemSubclass = None, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.itemName = itemName
        self.itemSubclass = itemSubclass
        self.quantity = str(quantity)
        self.initialize()
    
    def initialize(self):
        #Limit size of each total widget area
        self.setMaximumSize(320,100)
        self.setStyleSheet("""
                    BasketItem{
                        background-color: #90CF8E;
                        border: 5px solid #000000;
                        border-radius: 20px;
                        }
                        """)
        coreLayout = QHBoxLayout(self)
        coreLayout.setContentsMargins(5,2,2,5)
        internalInfo = QVBoxLayout()
        internalInfo.setContentsMargins(2,2,2,5)

        #Set item name and quantity in labels
        name = QLabel(self.itemName)
        name.setStyleSheet("""
            QLabel{
                background-color: #E4FDE1;
                border: 2px solid #000000;
                border-radius: 20px;
                font: 12pt 'Georgia';
                padding: 5px 5px 5px 5px;
            }""")
        name.setFixedSize(250,50)
        name.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        internalInfo.addWidget(name)

        #Sub-section containing quantity
        self.quantityLabel = QLabel(self.quantity)
        self.quantityLabel.setStyleSheet("""
            QLabel{
                background-color: #E4FDE1;
                border: 2px solid #000000;
                border-radius: 10px;
                font: 12pt 'Georgia';
            }""")
        self.quantityLabel.setFixedSize(30,30)
        self.quantityLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        internalInfo.addWidget(self.quantityLabel)
        coreLayout.addLayout(internalInfo)


        """Create edit and delete buttons
        We can add icons by using QIcon and paths to icon
        locations within images"""
        #Add edit button for item
        buttons = QVBoxLayout()
        buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        editButton = QPushButton(self)
        editButton.setIcon(QIcon("app/images/edit-icon.png"))
        editButton.setIconSize(QSize(25,25))
        editButton.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                                }
                                """)
        editButton.setFixedSize(45,45)
        editButton.clicked.connect(self.edit)
        buttons.addWidget(editButton)

        #Add delete button for item
        deleteButton = QPushButton(self)
        deleteButton.setIcon(QIcon("app/images/trash-icon.png"))
        deleteButton.setIconSize(QSize(25,25))
        deleteButton.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                                }
                                """)
        deleteButton.setFixedSize(45,45)
        deleteButton.clicked.connect(self.deleteItem)
        
        #Add buttons to button layout
        #Add that layout to the core layout and be done
        buttons.addWidget(deleteButton)
        coreLayout.addLayout(buttons)
        self.setLayout(coreLayout)

    #For getting itemName
    def getName(self):
        return self.itemName

    #Create a popup to confirm deleting an item from the list
    def deleteItem(self):
        dialog = deleteItemPopup(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.parent.deleteItem(self.itemName, int(self.quantity))
            self.deleteLater()

    #Create a popup to allow editing a list item
    def edit(self):
        dialog = editItemPopup(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            input = dialog.getInput()
            #Do update here
            self.parent.editItem(self.itemName, int(input))
            self.quantityLabel.setText(input)

    #Get list from shoppinglistpage
    def getList(self):
        self.parent.getList()

class addItem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.manageList = self.parent.getList()
        self.initialize()
    
    def initialize(self):
        #Initiate addItem
        self.setFixedSize(280,200)
        self.setStyleSheet("""
            addItem{ 
                background-color: #90CF8E;
                border: 5px solid #000000;
                border-radius: 20px; 
                                    }""")

        """These are all self because we want to reference
        them in other sub-functions"""
        #Name field
        layout = QVBoxLayout()
        self.nameField = QLineEdit()
        self.nameField.setContentsMargins(0,10,0,10)
        self.nameField.setFixedSize(263,75)
        self.nameField.setStyleSheet("""
            QLineEdit { 
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                font: 12pt 'Georgia';
                                      }""")
        self.nameField.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        
        #Quantity field
        self.quantityField = QLineEdit()
        self.quantityField.setContentsMargins(0,10,0,10)
        self.quantityField.setFixedSize(263,75)
        self.quantityField.setStyleSheet("""
            QLineEdit { 
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                font: 12pt 'Georgia';
                                      }""")
        self.quantityField.setAlignment(Qt.AlignmentFlag.AlignCenter)
        intValidator = QIntValidator(self)
        self.quantityField.setValidator(intValidator)

        #Make buttons
        #Cancel button closes popup without doing anything
        cancelButton = QPushButton("Cancel", self)
        cancelButton.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                padding: 5px;
                font: 8pt 'Georgia';
                                }
                                """)
        
        #Ok button confirms that we want to add this item
        okButton = QPushButton("Confirm", self)
        okButton.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                padding: 5px;
                font: 8pt 'Georgia';
                                }
                                """)
        
        #Tie buttons to actions
        #We want to confirm the inputs of the user are acceptable
        #Else don't allow for them to continue
        okButton.clicked.connect(self.validateBeforeAccept)  
        cancelButton.clicked.connect(self.customCancel)

        #Create layout for popup
        #Populate the layout
        layout.addWidget(self.nameField)
        layout.addWidget(self.quantityField)
        buttons = QHBoxLayout()
        buttons.addWidget(cancelButton)
        buttons.addWidget(okButton)
        layout.addLayout(buttons)
        self.setLayout(layout)

    def getName(self):
        return self.nameField.text()

    def getQuantity(self):
        return self.quantityField.text()

    #Close it, but update that the layout gets changed back
    def customCancel(self):
        self.parent.changeBaseLayout()

    #Ensure the inputs are valid
    def validateBeforeAccept(self):
        nameValidate = self.nameField.text()
        intValidate = self.quantityField.text()

        #Don't progress if either field is empty
        if not nameValidate or not intValidate:
            return
        else: 
            #Cast int and make sure its reasonable
            valueInt = int(intValidate)
            if (valueInt < 1 or valueInt > 100):
                return
            #Check with the built-in method or items
            elif (self.manageList.check_item_name(nameValidate) == False):
                return
            #If all is good call parent makeNewItem function
            #Update layout
            else:
                self.parent.makeNewItem()
                self.parent.changeBaseLayout()

class editItemPopup(QDialog):
    """Popups exist as temprary module windows"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        #Initiate popup
        self.setStyleSheet("""
            QDialog{ background: #E4FDE1; }""")
        self.setFixedSize(300,150)

        #Make customized buttons
        #Cancel button to end popup
        cancelButton = QPushButton("Cancel", self)
        cancelButton.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                padding: 5px;
                font: 8pt 'Georgia';
                                }
                                """)
        
        #Accept button to confirm popup
        confirmButton = QPushButton("Confirm", self)
        confirmButton.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                padding: 5px;
                font: 8pt 'Georgia';
                                }
                                """)
        
        #Tie buttons to actions
        cancelButton.clicked.connect(self.close)
        confirmButton.clicked.connect(self.accept)

        #Create layout for popup
        layout = QVBoxLayout()
        #Add central message
        itemName = self.parent.getName()
        message = QLabel("Edit item quantity for: "+itemName)
        message.setStyleSheet("""
            QLabel {
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                font: 12pt 'Georgia';
                                }
                                """)
        message.setMaximumHeight(100)
        message.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
        #Get new value for item
        self.inputField = QLineEdit()
        self.inputField.setFixedSize(277,50)
        self.inputField.setStyleSheet("""
            QLineEdit { 
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                font: 12pt 'Georgia';
                                      }""")
        self.inputField.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #Easier way to just make sure this value is between 1-100
        #Similar to our other validator
        intValidator = QIntValidator(1,100,self)
        self.inputField.setValidator(intValidator)
        #Populate the layout
        layout.addWidget(message)
        layout.addWidget(self.inputField)

        #Populate buttons
        buttons = QHBoxLayout()
        buttons.addWidget(cancelButton)
        buttons.addWidget(confirmButton)
        layout.addLayout(buttons)
        self.setLayout(layout)

    #For future reference
    def getInput(self):
        return self.inputField.text()

class deleteItemPopup(QDialog):
    """For deleting a list item"""
    def __init__(self, parent=None):
        super().__init__(parent)
        #Initiate popup
        self.setStyleSheet("""
            QDialog{ background: #E4FDE1; }""")
        self.setFixedSize(200,120)

        #Populate customized buttons
        #Cancel button
        cancelButton = QPushButton("Cancel", self)
        cancelButton.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                padding: 5px;
                                }
                                """)
        
        #Confirm button
        confirmButton = QPushButton("Yes, Delete", self)
        confirmButton.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                padding: 5px;
                                }
                                """)
        
        #Tie buttons to actions
        cancelButton.clicked.connect(self.close)
        confirmButton.clicked.connect(self.accept)

        #Create layout for popup
        layout = QVBoxLayout()
        #Add central message
        message = QLabel("Confirm Delete Item?")
        message.setStyleSheet("""
            QLabel {
                background-color: #E4FDE1;
                border: 2px solid #000000;
                color: black;
                border-radius: 8;
                font: 12pt 'Georgia';
                                }
                                """)
        message.setAlignment(Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignHCenter)
        
        #Populate the layout
        layout.addWidget(message)
        buttons = QHBoxLayout()
        buttons.addWidget(cancelButton)
        buttons.addWidget(confirmButton)
        layout.addLayout(buttons)
        self.setLayout(layout)

    #If we do indeed delete the item, 
    #First remove it from the page list_manager instance
    #Next delete the BasketItem widget instance
    def deleteParent(self):
        parent = self.parent()
        list = parent.getList()
        list.remove_item_from_list(parent.itemName, parent.quantity)
        parent.deleteLater()
        self.accept()

class CartItem(QWidget):
    """Same in all ways to the basket item but without buttons"""
    def __init__(self, itemName:str, quantity:int, itemSubclass = None, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.itemName = itemName
        self.itemSubclass = itemSubclass
        self.quantity = str(quantity)
        self.initialize()
    
    def initialize(self):
        self.setMaximumSize(320,100)
        self.setStyleSheet("""
                    BasketItem{
                        background-color: #90CF8E;
                        border: 5px solid #000000;
                        border-radius: 20px;
                        }
                        """)

        coreLayout = QHBoxLayout(self)
        coreLayout.setContentsMargins(10,2,2,5)
        
        internalInfo = QVBoxLayout()
        internalInfo.setContentsMargins(2,2,2,5)

        #Item name
        name = QLabel(self.itemName)
        name.setStyleSheet("""
            QLabel{
                background-color: #E4FDE1;
                border: 2px solid #000000;
                border-radius: 20px;
                font: 12pt 'Georgia';
                padding: 5px 5px 5px 5px;
            }""")
        name.setFixedSize(250,50)
        name.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        internalInfo.addWidget(name)

        #Quantity
        self.quantityLabel = QLabel(self.quantity)
        self.quantityLabel.setStyleSheet("""
            QLabel{
                background-color: #E4FDE1;
                border: 2px solid #000000;
                border-radius: 10px;
                font: 12pt 'Georgia';
            }""")
        self.quantityLabel.setFixedSize(30,30)
        self.quantityLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        internalInfo.addWidget(self.quantityLabel)
        coreLayout.addLayout(internalInfo)
        self.setLayout(coreLayout)