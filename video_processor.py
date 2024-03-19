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
      self.mode = "Color"
      self.capture_frame = False
      self.video_enabled = True
      self.video_inverted = True
      self.edge_detection_enabled = False

      # Define component labels
      self.btn_label_start = self.fetch_values("btn_label", "start")
      self.btn_label_pause = self.fetch_values("btn_label", "pause")
      self.btn_label_invert = self.fetch_values("btn_label", "invert")
      self.btn_label_save = self.fetch_values("btn_label", "save")
      self.btn_label_modes = ["Color", "Grayscale", "Edge detection", "Sepia Tone", "Sharpen", "Blur"]

      # Create components
      self.video_box = QGroupBox()
      self.video_frame = AspectLabel()
      self.pause_button = QPushButton()
      self.invert_button = QPushButton()
      self.save_button = QPushButton()
      self.mode_group = QButtonGroup()
      self.gs_threshold_slider = QSlider()
      self.ed_threshold_slider1 = QSlider()
      self.ed_threshold_slider2 = QSlider()
      self.gs_threshold_label = QLabel()
      self.ed_threshold_label1 = QLabel()
      self.ed_threshold_label2 = QLabel()
      self.vgap = QLabel()

      # Define component properties
      self.video_box.setObjectName("VideoBox")
      self.vgap.setObjectName("VerticalGap")
      self.mode_group.setExclusive(True)

      self.pause_button.setText(self.btn_label_pause)
      self.invert_button.setText(self.btn_label_invert)
      self.save_button.setText(self.btn_label_save)

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
      ctrl_layout = QHBoxLayout()
      ctrl_layout.addWidget(self.pause_button)
      ctrl_layout.addWidget(self.invert_button)
      ctrl_layout.addWidget(self.save_button)

      # Mode buttons layout
      mode_layout = QHBoxLayout()
      for mode in self.btn_label_modes:
        button = QPushButton(mode)
        mode_layout.addWidget(button)
        self.mode_group.addButton(button)

      # All buttons layout
      btn_layout = QVBoxLayout()
      btn_layout.addLayout(ctrl_layout)
      btn_layout.addLayout(mode_layout)

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

      # Parent layout
      layout = QVBoxLayout()
      layout.addWidget(self.video_box)
      layout.addLayout(btn_layout)
      layout.addWidget(self.vgap)
      layout.addLayout(gs_layout)
      layout.addLayout(ed_layout)
      self.setLayout(layout)

      # Enable button interactions
      self.pause_button.clicked.connect(self.enable_video)
      self.invert_button.clicked.connect(self.invert_video)
      self.save_button.clicked.connect(self.enable_capture)
      for mode_btn in self.mode_group.buttons():
        mode_btn.clicked.connect(self.handle_mode_change)

      # Enable timer 
      self.timer = QTimer()
      self.timer.timeout.connect(self.process_frame)

      # Enable webcam
      self.video_capture = cv2.VideoCapture(0)
      self.is_camera_connected = self.video_capture.isOpened()

      if not self.is_camera_connected:
        print("Application was unable to connect to webcam.")
        sys.exit()

      self.timer.start(30)

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

    # Fetch values
    def fetch_values(self, type, val):
      with open("values.json", "r") as file:
        values = json.load(file)

      return values[type][val]
    
    # Toggle mode
    def handle_mode_change(self):
        mode_button = self.sender()
        self.mode = mode_button.text()
        print(f"Button Pressed: Mode set to {self.mode}.")

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
          if self.mode == "Color":
            self.save_image(frame_rgb)
          elif self.mode == "Grayscale":
            self.save_image(frame_gray)
          elif self.mode == "Edge detection":
            self.save_image(edges)
          else:
            self.save_image(frame_rgb)

        # Choose display frame based on selected mode
        if self.mode == "Color":
          qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        elif self.mode == "Grayscale":
          qt_image = QImage(processed_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        elif self.mode == "Edge detection":
          qt_image = QImage(edges.data, w, h, QImage.Format_Grayscale8)
        else:
          qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Update button styles based on selected mode
        for mode_btn in self.mode_group.buttons():
          if mode_btn.text() == self.mode:
              mode_btn.setStyleSheet("background-color: #985eff;")
          else:
              mode_btn.setStyleSheet("background-color: #bb86fc;")
          
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