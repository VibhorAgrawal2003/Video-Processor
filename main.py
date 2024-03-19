import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from video_processor import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoProcessor()
    print("Application started")
    window.show()
    sys.exit(app.exec_())
