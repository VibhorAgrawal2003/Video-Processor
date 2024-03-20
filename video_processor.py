import cv2
import json
import os
import sys
import numpy as np
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
    self.btn_label_modes = self.fetch_values("btn_label", "modes")

    # Create components
    self.video_box = QGroupBox()
    self.video_frame = AspectLabel()
    self.pause_button = QPushButton()
    self.invert_button = QPushButton()
    self.save_button = QPushButton()
    self.mode_group = QButtonGroup()

    self.hue_slider = QSlider()
    self.saturation_slider = QSlider()
    self.brightness_slider = QSlider()
    self.bin_threshold_slider = QSlider()
    self.ed_threshold_slider1 = QSlider()
    self.ed_threshold_slider2 = QSlider()

    self.hue_label = QLabel()
    self.saturation_label = QLabel()
    self.brightness_label = QLabel()
    self.bin_threshold_label = QLabel()
    self.ed_threshold_label1 = QLabel()
    self.ed_threshold_label2 = QLabel()
    self.vgap = QLabel()
    self.hgap = QLabel()

    # Define component properties
    self.video_box.setObjectName("VideoBox")
    self.vgap.setObjectName("VerticalGap")
    self.hgap.setObjectName("HorizontalGap")
    self.mode_group.setExclusive(True)

    self.pause_button.setText(self.btn_label_pause)
    self.invert_button.setText(self.btn_label_invert)
    self.save_button.setText(self.btn_label_save)

    self.hue_slider.setOrientation(1)
    self.hue_slider.setMinimum(0)
    self.hue_slider.setMaximum(255)
    self.hue_slider.setValue(255)

    self.saturation_slider.setOrientation(1)
    self.saturation_slider.setMinimum(0)
    self.saturation_slider.setMaximum(255)
    self.saturation_slider.setValue(255)

    self.brightness_slider.setOrientation(1)
    self.brightness_slider.setMinimum(0)
    self.brightness_slider.setMaximum(255)
    self.brightness_slider.setValue(255)

    self.bin_threshold_slider.setOrientation(1)
    self.bin_threshold_slider.setMinimum(0)
    self.bin_threshold_slider.setMaximum(255)
    self.bin_threshold_slider.setValue(127)

    self.ed_threshold_slider1.setOrientation(1)
    self.ed_threshold_slider1.setMinimum(0)
    self.ed_threshold_slider1.setMaximum(255)
    self.ed_threshold_slider1.setValue(127)

    self.ed_threshold_slider2.setOrientation(1)
    self.ed_threshold_slider2.setMinimum(0)
    self.ed_threshold_slider2.setMaximum(255)
    self.ed_threshold_slider2.setValue(127)

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

    # Hue settings layout
    hue_layout = QVBoxLayout()
    hue_layout.addWidget(QLabel('Hue Slider'))
    hue_row_1 = QHBoxLayout()
    hue_row_1.addWidget(self.hue_slider)
    hue_row_1.addWidget(self.hue_label)
    hue_layout.addLayout(hue_row_1)

    # Saturation settings layout
    sat_layout = QVBoxLayout()
    sat_layout.addWidget(QLabel('Saturation Slider'))
    sat_row_1 = QHBoxLayout()
    sat_row_1.addWidget(self.saturation_slider)
    sat_row_1.addWidget(self.saturation_label)
    sat_layout.addLayout(sat_row_1)

    # Saturation settings layout
    bri_layout = QVBoxLayout()
    bri_layout.addWidget(QLabel('Brightness Slider'))
    bri_row_1 = QHBoxLayout()
    bri_row_1.addWidget(self.brightness_slider)
    bri_row_1.addWidget(self.brightness_label)
    bri_layout.addLayout(bri_row_1)

    # Binary settings layout
    bin_layout = QVBoxLayout()
    bin_layout.addWidget(QLabel('Binary Threshold Slider'))
    bin_row_1 = QHBoxLayout()
    bin_row_1.addWidget(self.bin_threshold_slider)
    bin_row_1.addWidget(self.bin_threshold_label)
    bin_layout.addLayout(bin_row_1)

    # Edge detection settings layout
    ed_layout = QVBoxLayout()
    ed_layout.addWidget(QLabel('Edge Detection Low Threshold Slider'))
    ed_row_1 = QHBoxLayout()
    ed_row_1.addWidget(self.ed_threshold_slider1)
    ed_row_1.addWidget(self.ed_threshold_label1)
    ed_layout.addLayout(ed_row_1)

    ed_layout.addWidget(QLabel('Edge Detection High Threshold Slider'))
    ed_row_2 = QHBoxLayout()
    ed_row_2.addWidget(self.ed_threshold_slider2)
    ed_row_2.addWidget(self.ed_threshold_label2)
    ed_layout.addLayout(ed_row_2)

    # Settings layout
    settings = QHBoxLayout()

    left_panel = QVBoxLayout()
    left_panel.addLayout(hue_layout)
    left_panel.addLayout(sat_layout)
    left_panel.addLayout(bri_layout)
    settings.addLayout(left_panel)
    
    settings.addWidget(self.hgap)

    right_panel = QVBoxLayout()
    right_panel.addLayout(bin_layout)
    right_panel.addLayout(ed_layout)
    settings.addLayout(right_panel)

    # Parent layout
    layout = QVBoxLayout()
    layout.addWidget(self.video_box)
    layout.addLayout(btn_layout)
    layout.addWidget(self.vgap)
    layout.addLayout(settings)
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
      self.pause_button.setStyleSheet("background-color: #bb86fc;")
      print("Button Pressed: Video stream started.")

    else:
      self.timer.stop()
      self.video_enabled = False
      self.pause_button.setText(self.btn_label_start)
      self.pause_button.setStyleSheet("background-color: #985eff;")
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
  
  # Toggle modes
  def handle_mode_change(self):
    mode_button = self.sender()
    self.mode = mode_button.text()
    print(f"Button Pressed: Mode set to {self.mode}.")

    if self.mode == self.btn_label_modes[0]:
      self.saturation_slider.setValue(255) # Color
    elif self.mode == self.btn_label_modes[1]:
      self.saturation_slider.setValue(0) # Grayscale

  # Save video frames
  def save_image(self):
    self.capture_frame = False
    file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg)")
    if not file_path:
      return

    pixmap = self.video_frame.pixmap()
    if pixmap.isNull():
      print("No image to save.")
      return
    qt_image = pixmap.toImage()

    if qt_image.save(file_path):
      print("Image saved successfully at:", file_path)
    else:
      print("Failed to save image.")

  # Handle video stream
  def process_frame(self):
    ret, frame = self.video_capture.read()
    if ret:
      
      # Convert webcam frame to different color frames
      frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # rgb color frame
      frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # grayscale frame
      frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # hsv color frame


      # Check and invert frames if video inversion is on
      if self.video_inverted:
        frame_rgb = cv2.flip(frame_rgb, 1)
        frame_hsv = cv2.flip(frame_hsv, 1)
        frame_gray = cv2.flip(frame_gray, 1)


      # Obtain necessary frame data
      h, w, ch = frame_rgb.shape
      bytes_per_line = ch * w


      # Set hue, saturation, brightness
      hue_value = self.hue_slider.value()
      brightness_value = self.brightness_slider.value()
      saturation_value = self.saturation_slider.value()

      self.hue_label.setText(str(hue_value))
      self.brightness_label.setText(str(brightness_value))
      self.saturation_label.setText(str(saturation_value))

      frame_hsv[:, :, 0] = frame_hsv[:, :, 0] * (hue_value/255)
      frame_hsv[:, :, 1] = frame_hsv[:, :, 1] * (saturation_value/255)
      frame_hsv[:, :, 2] = frame_hsv[:, :, 2] * (brightness_value/255)
      frame_bgr = cv2.cvtColor(frame_hsv, cv2.COLOR_HSV2BGR)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)


      # Set binary threshold from threshold slider
      bin_threshold_value = self.bin_threshold_slider.value()
      self.bin_threshold_label.setText(str(bin_threshold_value))
      _, thresholded_frame = cv2.threshold(frame_gray, bin_threshold_value, 255, cv2.THRESH_BINARY)
      frame_bin = cv2.cvtColor(thresholded_frame, cv2.COLOR_GRAY2RGB)


      # Set edges based on edge detection threshold sliders
      ed_threshold_low = self.ed_threshold_slider1.value()
      ed_threshold_high = self.ed_threshold_slider2.value()
      self.ed_threshold_label1.setText(str(ed_threshold_low))
      self.ed_threshold_label2.setText(str(ed_threshold_high))
      frame_ed = cv2.Canny(frame_gray, ed_threshold_low, ed_threshold_high)


      # Set sepia frame using sepia matrix transform
      sepia_matrix = np.array([[0.393, 0.769, 0.189],
                        [0.349, 0.686, 0.168],
                        [0.272, 0.534, 0.131]])
      frame_sp = cv2.transform(frame_rgb, sepia_matrix)
      frame_sp = np.clip(frame_sp, 0, 255)


      # Set blur frame using opencv blur function
      frame_blur = cv2.blur(frame_rgb, (10, 10))


      # Choose save frame based on selected mode
      if self.capture_frame:
        self.save_image()


      # Choose display frame based on selected mode
      if self.mode == self.btn_label_modes[0]:
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
      elif self.mode == self.btn_label_modes[1]:
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
      elif self.mode == self.btn_label_modes[2]:
        qt_image = QImage(frame_bin.data, w, h, bytes_per_line, QImage.Format_RGB888)
      elif self.mode == self.btn_label_modes[3]:
        qt_image = QImage(frame_ed.data, w, h, QImage.Format_Grayscale8)
      elif self.mode == self.btn_label_modes[4]:
        qt_image = QImage(frame_sp.data, w, h, bytes_per_line, QImage.Format_RGB888)
      elif self.mode == self.btn_label_modes[5]:
        qt_image = QImage(frame_blur.data, w, h, bytes_per_line, QImage.Format_RGB888)
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