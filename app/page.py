from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import cv2

from list_manager.list_manager import ListManager

class Page(QWidget):
    def __init__(self):
        super(Page, self).__init__()
        self.listManager = ListManager([0,0,0,0,0])
        self.initialize()
    
    def initialize(self):
        #Initialize the layout of the Page widget
        layout = QVBoxLayout(self)
        self.setStyleSheet("""background-color: #A7DCA5;""")
        layout.setContentsMargins(1,1,1,1)

        #Start a page controller which will allow us to swap pages
        self.pageController = QStackedWidget(self)

        #Initialize both pages
        homepage = HomePage(self)
        newlistpage = ShoppingListPage(self)

        #Add both pages to the controller
        self.pageController.addWidget(homepage)
        self.pageController.addWidget(newlistpage)

        #Finalize initialization of page
        #Set current page to home page
        self.changePage(0)
        #Active layout
        layout.addWidget(self.pageController)
        self.setLayout(layout)

    #Allow us to call change page from within individual pages
    def changePage(self, index):
        #Sets the controller index
        #0 is for home page
        #1 is for list/cart page
        self.clearLayout()
        self.pageController.setCurrentIndex(index)

    #This lets us reset layout of page if needed
    def clearLayout(self):
        self.layout().update()

    #Lets subpages reference list
    def getList(self):
        return self.listManager

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.initialize()
    
    def initialize(self):
        #Clear any past layout data
        if self.layout() is not None:
            self.parent.clearLayout()

        #Set basic page information
        self.setStyleSheet("""background-color: #A7DCA5;""")

        #Make encompassing layout
        """ Content margins just specify to not leave any 
        space between this page and the main "page" widget.
        Alternatively, content margins allow us to specify
        space between the current and previous widget
            Alignments let us specify where the center
        of the widget should line up
            Maximum sizes are the limits of the widget, 
        allowing for it to dynamically change to adjust
        for other content"""
        outerLayout = QVBoxLayout()
        outerLayout.setContentsMargins(0,0,0,0)

        #Make header layout
        header = QVBoxLayout()
        header.setContentsMargins(10,10,10,10)
        header.setAlignment(Qt.AlignmentFlag.AlignTop)

        #Make central content layout
        content = QVBoxLayout()
        content.setContentsMargins(10,10,10,10)
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)


        #Add picture to home screen
        #We do this by entering a pixmap with the path to the image
        picture = QLabel()
        picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pictureMap = QPixmap("app/images/Groceries.PNG")
        picture.setPixmap(pictureMap)
        picture.setScaledContents
        picture.setMaximumSize(360,360)
        header.addWidget(picture)

        #Make Page Header
        #We can set fonts and sizes without requiring stylesheets
        pageHeader = QLabel("Grocery Assistant")
        pageHeader.setFont(QFont("Georgia", 28))
        pageHeader.setMaximumHeight(100)

        #Center header & add extra top padding
        pageHeader.setContentsMargins(0,10,0,0)
        pageHeader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #Add content to the header,
        #Add header to the top layer of the page
        header.addWidget(pageHeader)
        outerLayout.addLayout(header)

        #Make navigation
        #Make Access List Bustton
        self.newListBtn = QPushButton("Shopping List", self)

        #Update style sheet to specify appearance of button 
        """Style sheets are a more dynamic way of setting
            multiple factors at once
            Must be led with class/subclass name"""
        self.newListBtn.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                color: black;
                border: 2px solid #90CF8E;
                border-radius: 14px;
                padding: 10px 20px;              
                font: 20pt 'Georgia'
                }
                                """)

        #Set maximum size of button
        self.newListBtn.setMaximumSize(360, 100)

        #Set button clicked result
        self.newListBtn.clicked.connect(self.goToNewListPage)

        #Add button to content section of page
        content.addWidget(self.newListBtn)

        #Initialize layout
        outerLayout.addLayout(content)
        self.setLayout(outerLayout)

    #Define parent function to change pages
    def goToNewListPage(self):
        self.parent.changePage(1)

    #Content for implementing CV:
    """def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to QImage
            height, width, _ = frame_rgb.shape
            qimg = QImage(frame_rgb.data, width, height, width * 3, QImage.Format.Format_RGB888)

            # Convert QImage to QPixmap and display it
            self.picture.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        # Release the video capture object when the window is closed
        self.cap.release()
        event.accept()

    self.picture = QLabel()
    self.cap = cv2.VideoCapture(0)
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.update_frame)
    self.timer.start(30)  # Update every 30ms (approx 30 frames per second)"""

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

        #Add video feed
        self.videoFeed = QLabel()
        self.videoFeed.setFixedHeight(300)
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30ms (approx 30 frames per second)
        self.outerLayout.addWidget(self.videoFeed)

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
                if quantity > 0:
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
                if quantity > 0:
                    temp = CartItem(item, quantity, parent=self)
                    self.shoppingCartContents.addWidget(temp)
                    self.outerLayout.update()

    #Delete an item from the list (parent function)
    def deleteItem(self, name, quantity):
        self.manageList.remove_item_from_list(name, quantity)

    #Edit an item from the list (parent function)
    def editItem(self, name, quantity):
        self.manageList.modify_quantity_of_list(name, quantity)

    #For running video frame
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to QImage
            height, width, _ = frame_rgb.shape
            qimg = QImage(frame_rgb.data, width, height, width * 3, QImage.Format.Format_RGB888)

            # Convert QImage to QPixmap and display it
            self.videoFeed.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        # Release the video capture object when the window is closed
        self.cap.release()
        event.accept()

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
        self.setFixedSize(280,180)
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
        self.nameField.setPlaceholderText("Item Name")
        self.nameField.setContentsMargins(0,10,0,5)
        self.nameField.setFixedSize(263,60)
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
        self.quantityField.setPlaceholderText("Item Quantity")
        self.quantityField.setContentsMargins(0,0,0,5)
        self.quantityField.setFixedSize(263,50)
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