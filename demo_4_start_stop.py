import cv2  # Importing OpenCV library for computer vision tasks
import tkinter as tk  # Importing tkinter for GUI
from datetime import datetime  # Importing datetime for timestamping
import threading  # Importing threading for multitasking


class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Streaming App")  # Setting up the window title

        # Initializing camera capture with index 0 (default webcam)
        self.camera = cv2.VideoCapture(0)
        self.is_streaming = False  # Flag for video streaming status
        self.rotation = 0  # Variable to store rotation angle

        # Creating GUI elements - video frame display and control buttons
        self.video_frame = tk.Label(root)
        self.video_frame.pack()

        self.start_button = tk.Button(
            root, text="Start Stream", command=self.start_stream)
        self.stop_button = tk.Button(
            root, text="Stop Stream", command=self.stop_stream)
        self.capture_button = tk.Button(
            root, text="Capture Image", command=self.capture_image)
        self.rotate_button = tk.Button(
            root, text="Rotate Video", command=self.rotate_video)

        # Packing the buttons in the window
        self.start_button.pack()
        self.stop_button.pack()
        self.capture_button.pack()
        self.rotate_button.pack()
        # Initializing the thread for video streaming
        self.stream_thread = None

    def start_stream(self):
        # Method to start video streaming
        if not self.is_streaming:
            self.is_streaming = True  # Setting the streaming flag
            # Disabling/enabling appropriate buttons
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.capture_button.config(state=tk.NORMAL)
            self.rotate_button.config(state=tk.NORMAL)

            # Creating a new thread for video streaming
            self.stream_thread = threading.Thread(target=self.stream_video)
            self.stream_thread.start()  # Starting the streaming thread

    def stop_stream(self):
        # Method to stop video streaming
        self.is_streaming = False  # Updating the streaming flag
        # Disabling/enabling appropriate buttons
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.capture_button.config(state=tk.DISABLED)
        self.rotate_button.config(state=tk.DISABLED)

    def stream_video(self):
        # Method to continuously stream video
        while self.is_streaming:  # While streaming flag is True
            ret, frame = self.camera.read()  # Reading frames from the camera
            if self.rotation != 0:  # If rotation angle is not 0
                frame = cv2.rotate(frame, self.rotation)  # Rotate the frame
            # Converting OpenCV frame to Tkinter image format
            img = tk.PhotoImage(data=cv2.imencode('.png', frame)[1].tobytes())
            # Displaying the image in the GUI video frame
            self.video_frame.config(image=img)
            self.video_frame.image = img  # Keeping a reference to the image

    def capture_image(self):
        # Method to capture and save an image from the video stream
        ret, frame = self.camera.read()  # Reading a single frame from the camera
        if self.rotation != 0:  # If rotation angle is not 0
            frame = cv2.rotate(frame, self.rotation)  # Rotate the frame
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Current timestamp
        filename = f"captured_{now}.png"  # Filename with timestamp
        cv2.imwrite(filename, frame)  # Save the frame as an image
        print(f"Captured and saved {filename}")  # Print a confirmation message

    def rotate_video(self):
        # Method to rotate the video frame by 90 degrees
        self.rotation = (self.rotation + 90) % 360  # Update the rotation angle


if __name__ == "__main__":
    # Creating the Tkinter window and initializing the CameraApp
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()  # Start the GUI event loop
