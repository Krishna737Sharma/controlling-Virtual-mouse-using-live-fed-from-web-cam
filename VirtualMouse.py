import cv2  # OpenCV library for image and video processing
import numpy as np  # NumPy library for handling arrays and numerical operations
import math  # Math library for mathematical functions
import time  # Time library for handling time-related functions
import pyautogui  # PyAutoGUI library for controlling the mouse and keyboard

# Disable PyAutoGUI's failsafe to prevent accidental interruptions when the mouse is moved to a corner
pyautogui.FAILSAFE = False

# Get the screen resolution of the display
SCREEN_X, SCREEN_Y = pyautogui.size()
print(f"Screen resolution: Width = {SCREEN_X}, Height = {SCREEN_Y}")  # Print the screen resolution

# Variables for mouse movement and click initialization
CLICK = CLICK_MESSAGE = MOVEMENT_START = None

# Capture video from the webcam (index 0 for the default camera)
cap = cv2.VideoCapture(0)

# Start the video stream loop
while cap.isOpened():
    ret, img = cap.read()  # Capture a frame from the webcam
    if not ret:
        break  # Exit if the frame is not captured properly

    CAMERA_X, CAMERA_Y, channels = img.shape  # Get the dimensions of the captured frame
    print(
        f"\nFrame {time.time()} - Camera resolution: Width = {CAMERA_Y}, Height = {CAMERA_X}")  # Print camera frame size

    img = cv2.flip(img, 1)  # Flip the image horizontally for a mirror effect
    crop_img = img  # Crop the image (no cropping applied, kept as the original)

    # Convert the frame to grayscale
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise in the image
    blurred = cv2.GaussianBlur(grey, (35, 35), 0)
    cv2.imshow('Blurred', blurred)
    # Apply Otsu's thresholding method to get a binary image (black and white)
    _, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imshow('Thresholded', thresh1)
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Initialize an empty drawing to hold the contours and hull
    drawing = np.zeros_like(img)
    max_area = -1  # Variable to track the largest contour area
    ci = -1  # Index of the largest contour

    # Initialize count_defects to 0 before counting defects
    count_defects = 0

    # Loop through the contours to find the largest one
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)  # Calculate the area of the contour
        if area > max_area:  # If the current contour has a larger area
            max_area = area  # Update the largest contour area
            ci = i  # Update the index of the largest contour
    print(f"Largest contour area: {max_area}")  # Print the largest contour area

    if ci != -1:  # If a valid contour is found
        # Get the largest contour
        cnt = contours[ci]

        # Get the bounding rectangle around the contour
        x, y, w, h = cv2.boundingRect(cnt)
        # Draw the bounding rectangle around the largest contour (in red)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        print(f"Bounding box: x={x}, y={y}, width={w}, height={h}")  # Print bounding box coordinates

        # Calculate the convex hull of the contour (the "outline")
        hull = cv2.convexHull(cnt)
        # Draw the contour and the convex hull (in green and red)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 2)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 2)

        # Find convexity defects in the contour
        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)
        used_defect = None  # Variable to store the defect point to use for gestures

        if defects is not None:  # If defects are found
            # Loop through the defects
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(cnt[s][0])  # Start point of the defect
                end = tuple(cnt[e][0])  # End point of the defect
                far = tuple(cnt[f][0])  # Far point of the defect

                # Calculate the sides of the triangle formed by the defect points
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

                # Calculate the angle between the three points
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

                # If the angle is less than or equal to 90 degrees, it's a valid defect
                if angle <= 90:
                    count_defects += 1  # Increment defect count for valid defects
                    cv2.circle(img, far, 5, [255, 0, 0], -1)  # Draw a blue circle for valid defects
                else:
                    cv2.circle(img, far, 5, [0, 255, 255], -1)  # Draw a yellow circle for non-valid defects

                # Draw lines between the start, end, and far points of the defect
                cv2.line(img, start, end, [0, 255, 0], 2)

                # Track the position of the first valid defect
                if count_defects == 2 and angle <= 90:
                    used_defect = {"x": start[0], "y": start[1]}

        print(f"Number of defects detected: {count_defects}")  # Print the number of valid defects

        # Perform actions based on the number of defects
        if used_defect is not None:
            x, y = used_defect["x"], used_defect["y"]
            if count_defects == 2:  # When two defects are detected, start mouse movement
                display_x = x
                display_y = y

                if MOVEMENT_START is not None:  # If a movement start point is defined
                    # Calculate the relative movement of the mouse
                    x = x - MOVEMENT_START[0]
                    y = y - MOVEMENT_START[1]
                    # Scale the movement based on the screen and camera resolutions
                    x = x * (SCREEN_X / CAMERA_Y)
                    y = y * (SCREEN_Y / CAMERA_X)
                    MOVEMENT_START = (display_x, display_y)  # Update movement start point
                    print(f"Moving Mouse to -> X: {x:.2f}, Y: {y:.2f}")  # Print the new mouse position
                    pyautogui.moveRel(x, y)  # Move the mouse relative to the previous position
                else:
                    MOVEMENT_START = (display_x, display_y)  # Set the movement start point

                # Draw a white circle at the defect position (for visualization)
                cv2.circle(img, (display_x, display_y), 10, [255, 255, 255], -1)

            elif count_defects == 3 and CLICK is None:  # When three defects are detected, perform left click
                CLICK = time.time()  # Record the time of the click
                pyautogui.click()  # Perform a left click
                CLICK_MESSAGE = "LEFT CLICK"
                print("Action: Left Click")  # Print the action performed
                cv2.putText(img, "Left Click", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print("Left Click")  # Explicit print for Left Click

            elif count_defects == 4 and CLICK is None:  # When four defects are detected, perform right click
                CLICK = time.time()  # Record the time of the click
                pyautogui.rightClick()  # Perform a right click
                CLICK_MESSAGE = "RIGHT CLICK"
                print("Action: Right Click")  # Print the action performed
                cv2.putText(img, "Right Click", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print("Right Click")  # Explicit print for Right Click
        else:
            MOVEMENT_START = None  # Reset the movement start point if no valid defects are found

    # Display the number of defects detected on the image
    cv2.putText(img, f"Defects: {count_defects}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    # If a click action was performed, reset it after some time has passed
    if CLICK is not None and CLICK < time.time():
        CLICK = None
    # Show the images: the original frame with gestures and the drawing with contours and defects
    cv2.imshow("Gesture", img)
    cv2.imshow("Drawing", drawing)

    # Exit the loop if the ESC key (ASCII value 27) is pressed
    k = cv2.waitKey(10)
    if k == 27:
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
