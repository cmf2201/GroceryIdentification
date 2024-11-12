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

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.