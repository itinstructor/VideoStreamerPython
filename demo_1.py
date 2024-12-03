# Import necessary libraries
import cv2  # Import OpenCV library for image processing
import tkinter as tk  # Import tkinter for creating GUI
from tkinter import ttk  # Import ttk module for themed widgets


class VideoCaptureApp:
    def __init__(self, root):
        # Initialize the application and set the window title
        self.root = root
        self.root.title("Video Capture App")

        # Create 'Start Capture' button and 'Quit' button using ttk.Button
        self.capture_button = ttk.Button(
            root, text="Start Capture", command=self.start_capture)
        # Place 'Start Capture' button in the window
        self.capture_button.pack(pady=10)

        self.quit_button = ttk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(pady=5)  # Place 'Quit' button in the window

        # Initialize variables for video capture and its status
        self.video_capture = None
        self.capture_active = False

    # Function to start or stop video capture
    def start_capture(self):
        if not self.capture_active:  # If capture is not active
            # Initialize video capture from default camera (index 0)
            self.video_capture = cv2.VideoCapture(0)
            self.capture_active = True  # Set capture status to active
            # Change button text to 'Stop Capture'
            self.capture_button.config(text="Stop Capture")
            self.update_video_stream()  # Call function to update video stream
        else:
            self.capture_active = False  # Set capture status to inactive
            self.video_capture.release()  # Release the video capture
            # Change button text to 'Start Capture'
            self.capture_button.config(text="Start Capture")

    # Function to continuously update the video stream
    def update_video_stream(self):
        if self.capture_active:  # If capture is active
            ret, frame = self.video_capture.read()  # Read a frame from the video capture
            if ret:  # If a frame is successfully read
                # Display the frame in a window named 'Video Stream'
                cv2.imshow('Video Stream', frame)
                # Schedule the next frame update after 10 milliseconds
                self.root.after(10, self.update_video_stream)
            else:
                self.stop_capture()  # If frame reading fails, stop the capture

    # Function to stop the video capture
    def stop_capture(self):
        if self.capture_active:  # If capture is active
            self.capture_active = False  # Set capture status to inactive
            self.video_capture.release()  # Release the video capture
            cv2.destroyAllWindows()  # Close all OpenCV windows
            # Change button text to 'Start Capture'
            self.capture_button.config(text="Start Capture")


# Main entry point of the program
if __name__ == "__main__":
    root = tk.Tk()  # Create a tkinter root window
    # Create an instance of the VideoCaptureApp class
    app = VideoCaptureApp(root)
    root.mainloop()  # Start the tkinter event loop to display the GUI and handle events
