# Import necessary libraries/modules
import cv2  # OpenCV library for video capturing and processing
import tkinter as tk  # Library for GUI
from tkinter import ttk  # Themed Tkinter widgets


class VideoCaptureApp:
    def __init__(self, root):
        # Initialize the root window for the application
        self.root = root
        self.root.title("Video Capture App")  # Set the title of the window

        # Create and place buttons in the GUI
        self.capture_button = ttk.Button(
            root, text="Start Capture", command=self.start_capture)
        self.capture_button.pack(pady=10)  # Adjust the position of the button

        self.quit_button = ttk.Button(root, text="Quit", command=self.quit)
        self.quit_button.pack(pady=5)  # Adjust the position of the button

        # Create a label to display the video stream
        self.video_frame = tk.Label(root)
        self.video_frame.pack()  # Place the label in the window

        # Initialize video capture variables
        self.video_capture = None  # Variable to hold the video capture object
        self.capture_active = False  # Flag to indicate if the capturing is active

    # Method to start/stop the video capture
    def start_capture(self):
        if not self.capture_active:  # If capture is not active
            # Open the default camera (index 0) for video capturing
            self.video_capture = cv2.VideoCapture(0)
            self.capture_active = True  # Set capture active flag to True
            self.capture_button.config(
                text="Stop Capture")  # Change button text
            self.update_video_stream()  # Start updating the video stream
        else:  # If capture is active
            self.capture_active = False  # Set capture active flag to False
            self.video_capture.release()  # Release the video capture object
            self.capture_button.config(
                text="Start Capture")  # Change button text

    # Method to continuously update the video stream
    def update_video_stream(self):
        if self.capture_active:  # If capture is active
            ret, frame = self.video_capture.read()  # Read a frame from the video capture
            if ret:  # If a frame is successfully captured
                # Convert the frame to a format compatible with Tkinter Label
                self.video_frame.imgtk = self.get_image(frame)
                # Update the label with the new frame
                self.video_frame.config(image=self.video_frame.imgtk)
                # Schedule the next frame update
                self.root.after(10, self.update_video_stream)
            else:  # If there's an issue capturing the frame
                self.stop_capture()  # Stop the video capture

    # Method to stop the video capture
    def stop_capture(self):
        if self.capture_active:  # If capture is active
            self.capture_active = False  # Set capture active flag to False
            self.video_capture.release()  # Release the video capture object
            cv2.destroyAllWindows()  # Close any OpenCV windows that might be open
            self.capture_button.config(
                text="Start Capture")  # Change button text

    # Method to quit the application
    def quit(self):
        if self.capture_active:  # If capture is active
            self.stop_capture()  # Stop the video capture
        self.root.quit()  # Quit the application

    # Method to convert a frame to a format compatible with Tkinter Label
    def get_image(self, frame):
        return tk.PhotoImage(data=cv2.imencode('.png', frame)[1].tobytes())


# Entry point of the program
if __name__ == "__main__":
    root = tk.Tk()  # Create the main Tkinter window
    app = VideoCaptureApp(root)  # Create an instance of the VideoCaptureApp
    root.mainloop()  # Start the GUI main loop for event handling
