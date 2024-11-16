import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from page import Page


#Class for main window
#Made with phone screen sizing in mind
#This will just hold the widgets

#Will need widget for each page which fits in main page
#Each individual page will have to contain the correct elements
class MainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()
        super(MainWindow, self).__init__()
        self.setFixedSize(375,667)
        self.setContentsMargins(0,0,0,0)

        #Start up Home Page
        driver = QWidget(self)
        self.setCentralWidget(driver)
        
        layout = QVBoxLayout()
        pageController = Page()
        layout.addWidget(pageController)
        driver.setLayout(layout)

#Pass in sys.argv to allow command line arguments
#QApplication([]) works with no command line
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  #Windows are hidden by default

# Start application loop.
app.exec()