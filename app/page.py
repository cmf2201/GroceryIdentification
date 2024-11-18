import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Page(QWidget):
    def __init__(self):
        super(Page, self).__init__()
        self.initialize()
    
    def initialize(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("""background-color: #A7DCA5;""")
        layout.setContentsMargins(1,1,1,1)

        #Start up Home Page
        self.pageController = QStackedWidget(self)

        homepage = HomePage(self)
        newlistpage = ShoppingListPage(self)

        self.pageController.addWidget(homepage)
        self.pageController.addWidget(newlistpage)
        self.changePage(0)
        layout.addWidget(self.pageController)
        self.setLayout(layout)


    def changePage(self, index):
        self.pageController.setCurrentIndex(index)

    def clearLayout(self):
        self.deleteLater(self.layout())

    def makeLabel(self, labelText, textSize = None):
        if(textSize == None):
            textSize = 28
        label = QLabel(labelText)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Georgia", textSize)
        label.setFont(font)
        label.setMinimumHeight(100)
        label.setMaximumHeight(150)

        label.setWordWrap(True)
        return label
    
    def makeNavButton(self, buttonText, buttonSize=None):
        button = QPushButton(buttonText, self)
        font = QFont("Georgia", 16)
        button.setFont(font)
        # button.setMinimumHeight(100)
        # button.setMaximumHeight(200)
        return button


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


        #Make picture
        picture = QLabel()
        picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pictureMap = QPixmap("app/images/Groceries.PNG")
        picture.setPixmap(pictureMap)
        picture.setScaledContents
        picture.setMaximumSize(360,360)
        header.addWidget(picture)

        #Make Page Header
        pageHeader = QLabel("Grocery Assistant")
        pageHeader.setFont(QFont("Georgia", 28))
        pageHeader.setMaximumHeight(100)

        #Center header & add extra top padding
        pageHeader.setContentsMargins(0,10,0,0)
        pageHeader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(pageHeader)
        outerLayout.addLayout(header)

        #Make navigation
        #If previous list exists

        #Make New List Option
        #Make new button
        #Update style sheet to specify appearance of button
        newListBtn = QPushButton("New Shopping List", self)
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

        #Set maximum size of button
        newListBtn.setMaximumSize(360, 100)

        #Set button clicked result
        newListBtn.clicked.connect(self.goToNewListPage)

        #Add button to content section of page
        content.addWidget(newListBtn)

        #Initialize layout
        outerLayout.addLayout(content)
        self.setLayout(outerLayout)

    def goToNewListPage(self):
        self.parent.changePage(1)


class ShoppingListPage(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.initialize()
    
    def initialize(self):
        #Clear any past layout data
        if self.layout() is not None:
            self.parent.clearLayout()

        #Setup layout
        self.setStyleSheet("""background-color: #A7DCA5;""")
        outerLayout = QVBoxLayout()
        outerLayout.setContentsMargins(0,0,0,0)
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

        outerLayout.addLayout(topLayer)

        #Make Page header
        pageLabel = QLabel("Current List")
        pageLabel.setFont(QFont("Georgia", 28))
        pageLabel.setMaximumHeight(50)
        pageLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        topLayer.addWidget(pageLabel)
        topLayer.setAlignment(Qt.AlignmentFlag.AlignTop)

        #Make section leader
        sectionHeader = QHBoxLayout()
        sectionHeader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #Potentially make 2 tabs?
        addFoodButton = QPushButton("Add Item", self)
        addFoodButton.setStyleSheet("""
            QPushButton {
                background-color: #E4FDE1;
                color: black;
                border-radius: 8;
                font: 16pt 'Georgia';
                                }
                                """)
        addFoodButton.setFixedSize(120,50)
        addFoodButton.clicked.connect(self.addFoodItem)
        sectionHeader.addWidget(addFoodButton)
        outerLayout.addLayout(sectionHeader)


        #Make Search Food Widget
        containerWidget = QWidget()
        contents = QScrollArea()
        contents.setWidgetResizable(True)
        contents.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        contents.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        contents.setWidget(containerWidget)
        shoppingListContents = QVBoxLayout()
        shoppingListContents.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        shoppingListContents.setSpacing(20)
        #Initialize basketItem instance
        #Add to shopingListContents

        # contents.setStyleSheet("""
        #                 background-color: #90CF8E;
        #                 border: 5px solid #EFFDEE;
        #                 border-radius: 20px;
        #                        """)
        
        # shoppingListContents.addWidget(contentHolder)

        
        item = BasketItem("granny smith", 4, self)
        item2 = BasketItem("mcintosh", 2, self)
        item3 = BasketItem("honeycrisp", 6, self)
        item4 = BasketItem("fuji", 1, self)
        item5 = BasketItem("gala", 2, self)
        item6 = BasketItem("golden delicious", 1, self)
        item7 = BasketItem("banana", 3, self)
        item8 = BasketItem("frozen banana", 1, self)
        shoppingListContents.addWidget(item)
        shoppingListContents.addWidget(item2)
        shoppingListContents.addWidget(item3)
        shoppingListContents.addWidget(item4)
        shoppingListContents.addWidget(item5)
        shoppingListContents.addWidget(item6)
        shoppingListContents.addWidget(item7)
        shoppingListContents.addWidget(item8)



        #Finalize page
        containerWidget.setLayout(shoppingListContents)
        outerLayout.addWidget(contents)
        self.setLayout(outerLayout)

    def gotToHomePage(self):
        self.parent.changePage(0)

    def addFoodItem(self):
        pass


class BasketItem(QWidget):
    def __init__(self, itemName, quantity, itemSubclass = None, parent=None):
        super().__init__()
        self.parent = parent
        self.itemName = itemName
        self.itemSubclass = itemSubclass
        self.quantity = str(quantity)
        self.initialize()
    
    def initialize(self):
        self.setFixedSize(320,100)
        self.setStyleSheet("""
                    BasketItem{
                        background-color: #90CF8E;
                        border: 5px solid #000000;
                        border-radius: 20px;
                        }
                        """)

        coreLayout = QHBoxLayout(self)
        coreLayout.setContentsMargins(10,2,2,5)
        
        # placeholderImg = QLabel()
        # placeholderImg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # placeholderMap = QPixmap("GroceryIdentification/app/Groceries.png")
        # placeholderImg.setPixmap(placeholderMap)
        # placeholderImg.setScaledContents
        # placeholderImg.setMaximumSize(80,80)
        # placeholderImg.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # coreLayout.addWidget(placeholderImg) 
        
        internalInfo = QVBoxLayout()
        internalInfo.setContentsMargins(2,2,2,5)

        #Do item name and quantity
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
        # itemHeader.addWidget(name)
        internalInfo.addWidget(name)

        #Sub-section
        quantity = QLabel(self.quantity)
        quantity.setStyleSheet("""
            QLabel{
                background-color: #E4FDE1;
                border: 2px solid #000000;
                border-radius: 10px;
                font: 12pt 'Georgia';
            }""")
        quantity.setFixedSize(30,30)
        quantity.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        internalInfo.addWidget(quantity)
        # if(self.itemSubclass != "" and self.itemSubclass is not None):
        #     itemDescription = QLabel(self.itemSubclass)
        #     itemDescription.setStyleSheet("""
        #         font: 10pt 'Georgia';
        #         text-align: center;""")
        #     itemDescription.setFixedSize(120,50)
        #     internalInfo.addWidget(itemDescription)

        coreLayout.addLayout(internalInfo)


        #Handle edit and delete buttons
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
        deleteButton.clicked.connect(self.deleteLater)
        buttons.addWidget(deleteButton)
        coreLayout.addLayout(buttons)


        self.setLayout(coreLayout)

#Should probably make confirmation popup
    def deleteItem(self):
        self.deleteLater()