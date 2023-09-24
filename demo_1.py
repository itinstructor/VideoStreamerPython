import cv2
import tkinter as tk
from tkinter import ttk


class VideoCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Capture App")

        self.capture_button = ttk.Button(
            root, text="Start Capture", command=self.start_capture)
        self.capture_button.pack(pady=10)

        self.quit_button = ttk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(pady=5)

        self.video_capture = None
        self.capture_active = False

    def start_capture(self):
        if not self.capture_active:
            self.video_capture = cv2.VideoCapture(0)
            self.capture_active = True
            self.capture_button.config(text="Stop Capture")
            self.update_video_stream()
        else:
            self.capture_active = False
            self.video_capture.release()
            self.capture_button.config(text="Start Capture")

    def update_video_stream(self):
        if self.capture_active:
            ret, frame = self.video_capture.read()
            if ret:
                cv2.imshow('Video Stream', frame)
                self.root.after(10, self.update_video_stream)
            else:
                self.stop_capture()

    def stop_capture(self):
        if self.capture_active:
            self.capture_active = False
            self.video_capture.release()
            cv2.destroyAllWindows()
            self.capture_button.config(text="Start Capture")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCaptureApp(root)
    root.mainloop()
