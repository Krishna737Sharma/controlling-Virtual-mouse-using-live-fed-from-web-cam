# controlling-Virtual-mouse-using-live-fed-from-web-cam
Sure! Below is a detailed `README.md` file for your gesture-controlled mouse project based on the code you provided:

---

# Gesture-Control-Mouse

This Python project allows users to control their computer's mouse cursor using hand gestures detected by the webcam. The program detects specific gestures such as moving the mouse and performing left and right clicks based on the number of defects in the hand's contours.

## Features

- **Mouse Movement:** Move the mouse cursor based on hand gestures.
- **Left Click:** Perform a left mouse click when the hand shows three defects.
- **Right Click:** Perform a right mouse click when the hand shows four defects.
- **Visual Feedback:** Displays real-time feedback on the webcam feed, showing detected defects and the corresponding actions (mouse movement, clicks).
- **Customizable Thresholds:** Customize the number of defects required for different actions.

## Requirements

- Python 3.x
- A webcam
- The following Python libraries:
  - `opencv-python` (for computer vision tasks)
  - `numpy` (for array manipulation)
  - `pyautogui` (for controlling the mouse and keyboard)

## Installation

To get started with this project, follow these steps:

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/gesture-control-mouse.git
cd gesture-control-mouse
```

### 2. Install Dependencies

Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

This will install the following dependencies:
- `opencv-python`
- `numpy`
- `pyautogui`

### 3. Set Up and Run the Code

After installing the dependencies, you can run the script:

```bash
python gesture_control.py
```

The program will open your webcam, and you will be able to control your mouse with hand gestures.

### 4. Usage

- **Mouse Movement:** Raise your hand in front of the camera. The program will track the number of defects (fingers) visible in the hand and use that information to move the mouse cursor.
- **Left Click:** When the program detects three defects (a "peace sign" or similar gesture), it will perform a left-click.
- **Right Click:** When the program detects four defects, it will perform a right-click.

### 5. Exiting the Program

To exit the program, simply press the **ESC** key while the video window is active.

---

## Code Walkthrough

1. **Camera Setup:**  
   The script uses OpenCV to capture the webcam feed in real-time. The webcam stream is flipped horizontally to create a mirror effect.

2. **Image Processing:**  
   The captured frames are converted to grayscale and blurred to reduce noise. Then, Otsu's thresholding is applied to create a binary image for contour detection.

3. **Contour Detection:**  
   The contours of the hand are detected using OpenCV's `findContours()` function. The largest contour (assumed to be the hand) is identified and used to track the number of defects.

4. **Convexity Defects:**  
   The program calculates convexity defects in the hand's contour, which corresponds to the spaces between the fingers. The number of defects determines the type of action (e.g., move, left click, right click).

5. **Mouse Actions:**  
   Based on the number of defects detected:
   - **2 defects**: Starts mouse movement.
   - **3 defects**: Performs a left click.
   - **4 defects**: Performs a right click.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Troubleshooting

- **Webcam not detected:** Ensure your webcam is properly connected and accessible.
- **Incorrect mouse movement:** The sensitivity and scaling of the mouse movement may need adjustment depending on your webcam resolution and screen size.
- **Gesture detection issues:** Ensure your hand is clearly visible in the camera frame. Proper lighting and a well-defined background help improve accuracy.

---

## Contributing

If you'd like to contribute to the project, feel free to fork the repository, create a pull request, or open an issue for any bugs or feature requests.

---

## Acknowledgments

- This project uses **OpenCV** for image processing and computer vision tasks.
- **PyAutoGUI** is used for simulating mouse actions based on hand gestures.

---

This `README.md` file provides a comprehensive guide for users to understand, install, and run your gesture-control-mouse project.
