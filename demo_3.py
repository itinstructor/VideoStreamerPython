import cv2
import tkinter as tk
from tkinter import ttk
import threading

class VideoCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Capture App")

        self.capture_button = ttk.Button(root, text="Start Capture", command=self.toggle_capture)
        self.capture_button.pack(pady=10)

        self.quit_button = ttk.Button(root, text="Quit", command=self.quit)
        self.quit_button.pack(pady=5)

        self.video_frame = tk.Label(root)
        self.video_frame.pack()

        self.video_capture = None
        self.capture_active = False
        self.toggle_capture()

    def toggle_capture(self):
        if not self.capture_active:
            self.capture_active = True
            self.capture_button.config(text="Stop Capture")
            self.capture_thread = threading.Thread(target=self.start_capture)
            self.capture_thread.start()
        else:
            self.capture_active = False
            self.capture_button.config(text="Start Capture")

    def start_capture(self):
        self.video_capture = cv2.VideoCapture(0)
        while self.capture_active:
            ret, frame = self.video_capture.read()
            if ret:
                self.root.after(10, self.update_video_frame, frame)
        self.video_capture.release()
        cv2.destroyAllWindows()

    def update_video_frame(self, frame):
        if self.capture_active:
            self.video_frame.imgtk = self.get_image(frame)
            self.video_frame.config(image=self.video_frame.imgtk)

    def quit(self):
        if self.capture_active:
            self.toggle_capture()
        self.root.quit()

    def get_image(self, frame):
        return tk.PhotoImage(data=cv2.imencode('.png', frame)[1].tobytes())

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCaptureApp(root)
    root.mainloop()
