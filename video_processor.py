import cv2
import json
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from components.labels import AspectLabel

class VideoProcessor(QWidget):
    def __init__(self):
    
      # Construct parent widget
      super().__init__()

      # Define properties
      self.setWindowTitle("Video Processor")
      self.setMaximumSize(1024, 768)
      self.mode = "color"
      self.capture_frame = False
      self.video_enabled = True
      self.video_inverted = True
      self.edge_detection_enabled = False

      # Define component labels
      self.btn_label_start = self.fetch_values("btn_label", "start")
      self.btn_label_pause = self.fetch_values("btn_label", "pause")
      self.btn_label_invert = self.fetch_values("btn_label", "invert")
      self.btn_label_save = self.fetch_values("btn_label", "save")
      self.btn_label_color = self.fetch_values("btn_label", "color")
      self.btn_label_grayscale = self.fetch_values("btn_label", "grayscale")
      self.btn_label_edge_enable = self.fetch_values("btn_label", "edge_enable")
      self.btn_label_edge_disable = self.fetch_values("btn_label", "edge_disable")

      # Create components
      self.video_box = QGroupBox()
      self.video_frame = AspectLabel()
      self.pause_button = QPushButton()
      self.invert_button = QPushButton()
      self.save_button = QPushButton()
      self.grayscale_button = QPushButton()
      self.edge_detection_button = QPushButton()
      self.gs_threshold_slider = QSlider()
      self.ed_threshold_slider1 = QSlider()
      self.ed_threshold_slider2 = QSlider()
      self.gs_threshold_label = QLabel()
      self.ed_threshold_label1 = QLabel()
      self.ed_threshold_label2 = QLabel()

      # Define component object names
      self.video_box.setObjectName("VideoBox")

      self.pause_button.setText(self.btn_label_pause)
      self.invert_button.setText(self.btn_label_invert)
      self.save_button.setText(self.btn_label_save)
      self.grayscale_button.setText(self.btn_label_grayscale)
      self.edge_detection_button.setText(self.btn_label_edge_enable)

      self.gs_threshold_slider.setOrientation(1)
      self.gs_threshold_slider.setMinimum(0)
      self.gs_threshold_slider.setMaximum(255)
      self.gs_threshold_slider.setValue(127)

      self.ed_threshold_slider1.setOrientation(1)
      self.ed_threshold_slider1.setMinimum(0)
      self.ed_threshold_slider1.setMaximum(255)
      self.ed_threshold_slider1.setValue(100)

      self.ed_threshold_slider2.setOrientation(1)
      self.ed_threshold_slider2.setMinimum(0)
      self.ed_threshold_slider2.setMaximum(255)
      self.ed_threshold_slider2.setValue(200)

      # Video display layout
      disp_layout = QVBoxLayout()
      disp_layout.addWidget(self.video_frame)
      self.video_box.setLayout(disp_layout)

      # Control buttons layout
      btn_row_1 = QHBoxLayout()
      btn_row_1.addWidget(self.pause_button)
      btn_row_1.addWidget(self.invert_button)
      btn_row_1.addWidget(self.save_button)

      btn_row_2 = QHBoxLayout()
      btn_row_2.addWidget(self.grayscale_button)
      btn_row_2.addWidget(self.edge_detection_button)
      
      btn_layout = QVBoxLayout()
      btn_layout.addLayout(btn_row_1)
      btn_layout.addLayout(btn_row_2)

      # Grayscale settings layout
      gs_layout = QVBoxLayout()
      gs_layout.addWidget(QLabel('Grayscale Threshold'))
      gs_row_1 = QHBoxLayout()
      gs_row_1.addWidget(self.gs_threshold_slider)
      gs_row_1.addWidget(self.gs_threshold_label)
      gs_layout.addLayout(gs_row_1)

      # Edge detection settings layout
      ed_layout = QVBoxLayout()
      ed_layout.addWidget(QLabel('Edge Detection Low Threshold'))
      ed_row_1 = QHBoxLayout()
      ed_row_1.addWidget(self.ed_threshold_slider1)
      ed_row_1.addWidget(self.ed_threshold_label1)
      ed_layout.addLayout(ed_row_1)

      ed_layout.addWidget(QLabel('Edge Detection High Threshold'))
      ed_row_2 = QHBoxLayout()
      ed_row_2.addWidget(self.ed_threshold_slider2)
      ed_row_2.addWidget(self.ed_threshold_label2)
      ed_layout.addLayout(ed_row_2)

      # Define parent layout
      layout = QVBoxLayout()
      layout.addWidget(self.video_box)
      layout.addLayout(btn_layout)
      layout.addLayout(gs_layout)
      layout.addLayout(ed_layout)
      self.setLayout(layout)

      # Enable button interactions
      self.pause_button.clicked.connect(self.enable_video)
      self.invert_button.clicked.connect(self.invert_video)
      self.save_button.clicked.connect(self.enable_capture)
      self.grayscale_button.clicked.connect(self.enable_greyscale)
      self.edge_detection_button.clicked.connect(self.enable_edge_detection)

      # Enable timer 
      self.timer = QTimer()
      self.timer.timeout.connect(self.process_frame)

      # Enable webcam
      self.video_capture = cv2.VideoCapture(0)
      self.is_camera_connected = self.video_capture.isOpened()

      if not self.is_camera_connected:
          print("Application was unable to connect to webcam.")
          sys.exit()

      self.timer.start(30)  # Update frame every 30ms

    # Pause button
    def enable_video(self):
      if not self.video_enabled:
        self.timer.start(30)
        self.video_enabled = True
        self.pause_button.setText(self.btn_label_pause)
        print("Button Pressed: Video stream started.")

      else:
        self.timer.stop()
        self.video_enabled = False
        self.pause_button.setText(self.btn_label_start)
        print("Button Pressed: Video stream paused.")

    # Invert button
    def invert_video(self):
      self.video_inverted = not self.video_inverted
      print("Button pressed: Video stream inverted.")

    # Save button
    def enable_capture(self):
      self.capture_frame = True
      if not self.video_enabled:
        self.enable_video()


    # Grayscale button
    def enable_greyscale(self):
      if self.mode == "color":
        self.mode = "grayscale"
        self.grayscale_button.setText(self.btn_label_color)
        print("Button Pressed: Switched to grayscale mode.")

      elif self.mode == "grayscale":
        self.mode = "color"
        self.grayscale_button.setText(self.btn_label_grayscale)
        print("Button Pressed: Switched to color mode.")

    # Edge detection button
    def enable_edge_detection(self):
      if not self.edge_detection_enabled:
        self.edge_detection_enabled = True
        self.edge_detection_button.setText(self.btn_label_edge_disable)
        print("Button Pressed: Edge detection turned ON.")

      else:
        self.edge_detection_enabled = False
        self.edge_detection_button.setText(self.btn_label_edge_enable)
        print("Button Pressed: Edge detection turned OFF.")

    # Fetch values
    def fetch_values(self, type, val):
      with open("values.json", "r") as file:
        values = json.load(file)

      return values[type][val]

    # Save video frames
    def save_image(self, image):
      self.capture_frame = False
      file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg)")
      if not file_path:
        return
      else:
        cv2.imwrite(file_path, image)
        print("Image saved successfully at:", file_path)

    # Handle video stream
    def process_frame(self):
      ret, frame = self.video_capture.read()
      if ret:
        
        # Convert webcam frame to different color frames
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # color frame
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # grayscale frame

        # Check and invert frames if video inversion is on
        if self.video_inverted:
          frame_rgb = cv2.flip(frame_rgb, 1)
          frame_gray = cv2.flip(frame_gray, 1)

        # Obtain necessary frame data
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w

        # Set grayscale threshold from threshold slider
        gs_threshold_value = self.gs_threshold_slider.value()
        self.gs_threshold_label.setText(str(gs_threshold_value))
        _, thresholded_frame = cv2.threshold(frame_gray, gs_threshold_value, 255, cv2.THRESH_BINARY)
        processed_frame = cv2.cvtColor(thresholded_frame, cv2.COLOR_GRAY2RGB)

        # Set edges based on edge detection threshold sliders
        ed_threshold_low = self.ed_threshold_slider1.value()
        ed_threshold_high = self.ed_threshold_slider2.value()
        self.ed_threshold_label1.setText(str(ed_threshold_low))
        self.ed_threshold_label2.setText(str(ed_threshold_high))
        edges = cv2.Canny(frame_gray, ed_threshold_low, ed_threshold_high)

        # Choose save frame based on selected mode
        if self.capture_frame:
          if self.edge_detection_enabled:
            self.save_image(edges)
          else:
            if self.mode == "color":
              self.save_image(frame_rgb)
            elif self.mode == "grayscale":
              self.save_image(processed_frame)

        # Choose display frame based on selected mode
        if self.edge_detection_enabled:
          qt_image = QImage(edges.data, w, h, QImage.Format_Grayscale8)
        else:
          if self.mode == "color":
              qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
          elif self.mode == "grayscale":
              qt_image = QImage(processed_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Convert selected frame to pixel map
        pixmap = QPixmap.fromImage(qt_image)
        self.video_frame.setPixmap(pixmap)
        self.video_frame.setScaledContents(True)

    # Close video stream
    def closeEvent(self, event):
      self.timer.stop()
      if self.video_capture.isOpened():
        self.video_capture.release()
      event.accept()