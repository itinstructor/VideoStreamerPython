# Import the OpenCV library for computer vision tasks
import cv2 


def start_video_capture():
    # Create a video capture object for the default camera (index 0)
    video_capture = cv2.VideoCapture(0)

    # Loop to continuously capture frames from the video feed
    while True:
        # Read a frame from the video capture
        ret, frame = video_capture.read()

        # Check if the frame is successfully read
        if not ret:
            break  # If unsuccessful, exit the loop

        # Display the captured frame in a window titled 'Video Stream'
        cv2.imshow('Video Stream', frame)

        # Wait for user input for 1 millisecond and capture the key pressed
        key = cv2.waitKey(1) & 0xFF

        # Check if the user pressed 'q' to quit the video capture
        if key == ord('q'):
            break  # If 'q' is pressed, exit the loop
        
        # Check if the user pressed 's' to stop the video capture
        elif key == ord('s'):
        
            # Release the video capture resources
            video_capture.release()
        
            # Close all OpenCV windows
            cv2.destroyAllWindows()
            return  # Exit the function and stop the video capture

    # Release the video capture resources
    video_capture.release()
    
    # Close all OpenCV windows
    cv2.destroyAllWindows()


# Main loop to prompt the user for starting or quitting video capture
while True:
    print("Press 's' to start video capture, 'q' to quit:")
    user_input = input()  # Get user input

    # Check user input to start or quit video capture
    if user_input == 's':
        start_video_capture()  # Call the function to start video capture
    elif user_input == 'q':
        break  # If 'q' is pressed, exit the main loop
