# Import necessary libraries/modules
import cv2  # OpenCV library for computer vision tasks
import tkinter as tk  # Tkinter library for creating GUI applications
from tkinter import ttk  # ttk module for themed widgets in Tkinter
import threading  # threading module for managing threads in Python


class VideoCaptureApp:
    def __init__(self, root):
        # Initialize the VideoCaptureApp with a root window
        self.root = root
        # Set the title of the application window
        self.root.title("Video Capture App")

        # Create buttons for starting/stopping capture and quitting the app
        self.capture_button = ttk.Button(
            root, text="Start Capture", command=self.toggle_capture)
        self.capture_button.pack(pady=10)  # Display the capture button

        self.quit_button = ttk.Button(root, text="Quit", command=self.quit)
        self.quit_button.pack(pady=5)  # Display the quit button

        # Create a label to display the video feed
        self.video_frame = tk.Label(root)
        self.video_frame.pack()  # Display the video frame label

        # Initialize variables for video capture and status
        self.video_capture = None
        self.capture_active = False
        self.toggle_capture()  # Start capturing video by default

    # Method to toggle between starting and stopping video capture
    def toggle_capture(self):
        if not self.capture_active:  # If capture is inactive
            self.capture_active = True  # Set capture status to active
            self.capture_button.config(
                text="Stop Capture")  # Update button text
            # Create a separate thread to start video capture
            self.capture_thread = threading.Thread(target=self.start_capture)
            self.capture_thread.start()  # Start the capture thread
        else:  # If capture is active
            self.capture_active = False  # Set capture status to inactive
            self.capture_button.config(
                text="Start Capture")  # Update button text

    # Method to start video capture
    def start_capture(self):
        # Open video capture device (default webcam)
        self.video_capture = cv2.VideoCapture(0)
        while self.capture_active:  # While capture is active
            ret, frame = self.video_capture.read()  # Read a frame from the video capture
            if ret:  # If a frame is successfully read
                # Update the video frame in the GUI after a delay of 10 milliseconds
                self.root.after(10, self.update_video_frame, frame)
        self.video_capture.release()  # Release the video capture device
        cv2.destroyAllWindows()  # Close all OpenCV windows

    # Method to update the video frame in the GUI
    def update_video_frame(self, frame):
        if self.capture_active:  # If capture is active
            # Convert the OpenCV frame to a format compatible with Tkinter
            self.video_frame.imgtk = self.get_image(frame)
            # Update the video frame
            self.video_frame.config(image=self.video_frame.imgtk)

    # Method to quit the application
    def quit(self):
        if self.capture_active:  # If capture is active
            self.toggle_capture()  # Stop the capture
        self.root.quit()  # Quit the application

    # Method to convert an OpenCV frame to a Tkinter-compatible image
    def get_image(self, frame):
        return tk.PhotoImage(data=cv2.imencode('.png', frame)[1].tobytes())


# Main section to run the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = VideoCaptureApp(root)  # Initialize the VideoCaptureApp
    root.mainloop()  # Start the main event loop for the application
