import cv2
import tkinter as tk
from datetime import datetime
import threading

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Streaming App")

        self.camera = cv2.VideoCapture(0)
        self.is_streaming = False
        self.rotation = 0

        self.video_frame = tk.Label(root)
        self.video_frame.pack()

        self.start_button = tk.Button(root, text="Start Stream", command=self.start_stream)
        self.stop_button = tk.Button(root, text="Stop Stream", command=self.stop_stream)
        self.capture_button = tk.Button(root, text="Capture Image", command=self.capture_image)
        self.rotate_button = tk.Button(root, text="Rotate Video", command=self.rotate_video)

        self.start_button.pack()
        self.stop_button.pack()
        self.capture_button.pack()
        self.rotate_button.pack()

        self.stream_thread = None

    def start_stream(self):
        if not self.is_streaming:
            self.is_streaming = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.capture_button.config(state=tk.NORMAL)
            self.rotate_button.config(state=tk.NORMAL)

            self.stream_thread = threading.Thread(target=self.stream_video)
            self.stream_thread.start()

    def stop_stream(self):
        self.is_streaming = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.capture_button.config(state=tk.DISABLED)
        self.rotate_button.config(state=tk.DISABLED)

    def stream_video(self):
        while self.is_streaming:
            ret, frame = self.camera.read()
            if self.rotation != 0:
                frame = cv2.rotate(frame, self.rotation)
            img = tk.PhotoImage(data=cv2.imencode('.png', frame)[1].tobytes())
            self.video_frame.config(image=img)
            self.video_frame.image = img

    def capture_image(self):
        ret, frame = self.camera.read()
        if self.rotation != 0:
            frame = cv2.rotate(frame, self.rotation)
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"captured_{now}.png"
        cv2.imwrite(filename, frame)
        print(f"Captured and saved {filename}")

    def rotate_video(self):
        self.rotation = (self.rotation + 90) % 360

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
