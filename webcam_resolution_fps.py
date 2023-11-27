# Import necessary libraries
import cv2  # OpenCV library for image processing
import time  # Library for time-related functions

# Initialize the camera at index 0 (usually the default webcam)
cam = cv2.VideoCapture(0)

# Variable to count the number of frames processed
num_frame = 0

# List of resolutions to test
resolution = [
    (640, 480), (640, 480), (704, 680), (800, 600), (960, 680),
    (1280, 720), (1440, 720), (1920, 1080)
]

# Loop through each resolution in the 'resolution' list
for i, j in enumerate(resolution):
    # Set the camera resolution to the current resolution being tested
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, j[0])
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, j[1])

    # Get the actual width and height set for the camera
    w = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Print the current resolution being tested
    print(f"Resolution: {w} x {h}")

    # Start time to measure performance
    start = time.time()

    # Loop to capture frames and calculate frames per second (fps)
    while True:
        # Read a frame from the camera
        ret, frame = cam.read()

        # Check if less than 60 frames have been processed
        if num_frame < 60:
            num_frame += 1
        else:
            # Calculate total processing time and frames per second (fps)
            total_time = (time.time() - start)
            fps = (num_frame / total_time)
            print(f"{num_frame} Frames {total_time:.2f} Seconds: {fps:.2f} fps")
            break

# Release the camera resource
cam.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
