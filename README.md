# Video Processor

This is a video capture and processing application designed to connect to the webcam or any other default capture peripheral connected to the device and display the video feed in real-time. Users can save individual frames from the video and apply various effects to enhance or modify the video stream.
<br>

## How It Works
The Video Processor application utilizes the PyQT5 framework for building the graphical user interface and CSS styling to enhance the visual appearance of the end-user application. Image processing is performed using the OpenCV library, providing efficient and powerful tools for manipulating video frames.
<br>

## Getting Started
To start using the Video Processor application, follow these steps:


1. To install all necessary dependencies, run the following command:
    ```bash
    pip install -r requirements.txt
    ```

    If this fails, you can install dependencies manually by running:
    ```bash
    pip install opencv-python-headless pyqt5
    ```
<br>

2. Navigate to the working directory using the `cd` command. Ensure that the path is correct via `pwd` and check contents of the directory via `ls` on Linux based systems and `dir` on Windows.
<br>

3. Run the main Python script using the command:
    ```bash
    python3 main.py
    ```
This will launch the Video Processor application.
<br>

## Controls and Buttons

The application provides various buttons and sliders to change the video display. Following is a brief description of available options:

- **Pause/Start video stream** 
Start or Stop the video display.
<br>

- **Invert camera**
Flips the video display horizontally.
<br>

- **Save current frame:**
Save the current video frame to any directory.
<br>

- **Color**
Set display mode to color (default), by adjusting hue and saturation.
<br>

- **Grayscale**
Set display mode to grayscale, by adjusting saturation to zero.
<br>

- **Edge detection**
Set display mode to edge detection. Use the two edge detection sliders to adjust the 'low' and 'high' threshold values for the Canny Algorithm.
<br>

- **Sepia Tone**
Set display mode to sepia tone.
<br>

- **Blur**
Set display mode to blur.
<br>


## Issues and Support
If you encounter any issues or bugs while using the Video Processor application, kindly contact me so I may work on the fixes. Cheers!
<br>
