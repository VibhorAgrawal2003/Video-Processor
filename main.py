import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from video_processor import *

def on_quit():
    print("Application closed")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoProcessor()

    # Add CSS styling to application
    with open('style.css', 'r') as file:
        style_sheet = file.read()
    window.setStyleSheet(style_sheet)

    # Connect to on_quit function
    app.aboutToQuit.connect(on_quit)

    # Start the application
    window.show()
    print("Application started")

    # Stop the application
    sys.exit(app.exec_())
