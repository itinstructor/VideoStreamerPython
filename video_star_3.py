#!/usr/bin/env python3
"""
    Name: video_star_2.py
    Author: 
    Created: 08/01/23
    Purpose: Stream video to a Tkinter interface using opencv

------------------------------------------------
History
------------------------------------------------
Author     Date           Comments

"""
# Raspberry Pi/Linux
# sudo apt install libatlas-base-dev -y
# sudo pip3 install numpy -U
# sudo pip3 install opencv-python
# Raspberry Pi Buster
# sudo pip3 install opencv-python==4.3.0.38

# Windows
# sudo pip3 install opencv-python
# sudo pip3 install pillow -U
# sudo pip3 install numpy -U
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk
import cv2
# Save and load configuration
import configparser
import os
# For image file time stamp
import time


class VideoStar():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Video Star OpenCV")
        # Set window location at 350x50 for pi zero
        # 600x50 pi
        self.root.geometry("+600+50")
        # Call self.quit when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Create VideoCapture object 0 = 1st camera
        self.cam = cv2.VideoCapture(0)
        # Start streaming flag to false
        self.streaming = False
        self.rotation_angle = 0
        self.load_settings()

        self.create_widgets()
        self.root.mainloop()

# ----------------------- START STOP VIDEO STREAM -------------------------#
    def start_stop_stream(self):
        """Stop or start the video stream"""
        if not self.streaming:
            self.start_stream()
        else:
            self.stop_stream()

# ------------------------ STOP VIDEO STREAM ------------------------------#
    def stop_stream(self):
        """Stop video stream"""
        self.streaming = False
        self.btn_start_stop.configure(text="Start Stream")
        # Release the camera capture object
        if self.cam.isOpened():
            self.cam.release()
        self.lbl_status_bar.configure(text=" Video Stream Stopped")

# ----------------------- START VIDEO CAPTURE -----------------------------#
    def start_stream(self):
        """Start video stream"""
        self.streaming = True
        self.lbl_status_bar.configure(text=" Video Stream Starting Up . . .")
        self.lbl_status_bar.update()
        self.btn_start_stop.configure(text="Stop Stream")
        self.lbl_status_bar.configure(text=" Video Stream Running . . .")
        self.update_stream()

# ------------------------ UPDATE STREAM ----------------------------------#
    def update_stream(self):
        """Read camera image frame by frame to update video stream"""
        if self.streaming:
            # Read camera image frame by frame
            # ret: Is a frame available True
            # frame: captured image
            ret, frame = self.cam.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                if self.rotation_angle != 0:
                    image = image.rotate(self.rotation_angle)
                photo = ImageTk.PhotoImage(image=image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.stream = photo
                self.display_fps()
            else:
                self.lbl_status_bar.configure(text=" Failed to grab frame")
                # # Convert cv2 colorspace BGR to RGB
                # self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        # Update video stream every 10 ms when the main program isn't busy
        self.root.after(10, self.update_stream)

# ---------------------- TAKE SNAPSHOT ------------------------------------#
    def snapshot(self):
        """Get and write a single video frame to a jpg image"""
        # Get a frame from the video source
        ret, frame = self.cam.read()

        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            if self.rotation_angle != 0:
                image = image.rotate(self.rotation_angle)

            filename = f"capture_{time.strftime('%Y%m%d%H%M%S')}.jpg"
            image.save(filename)
            print(f"Image saved as {filename}")

# --------------------------- ROTATE IMAGE --------------------------------#
    def rotate_image(self):
        """Rotate the incoming camera image"""
        self.rotation_angle += 90
        if self.rotation_angle >= 360:
            self.rotation_angle = 0
        self.save_settings()

# --------------------------- SAVE SETTINGS -------------------------------#
    def save_settings(self):
        """Save program settings for RotationAngle"""
        config = configparser.ConfigParser()
        config['Settings'] = {'RotationAngle': str(self.rotation_angle)}

        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

# --------------------------- LOAD SETTINGS -------------------------------#
    def load_settings(self):
        """Load program settings for RotationAngle"""
        if os.path.exists('settings.ini'):
            config = configparser.ConfigParser()
            config.read('settings.ini')
            if 'Settings' in config:
                rotation_angle = config['Settings'].get('RotationAngle', '0')
                self.rotation_angle = int(rotation_angle)

# --------------------------- DISPLAY FPS ---------------------------------#
    def display_fps(self):
        """Get and display FPS"""
        # Get frames per second from cam capture properties
        self.fps = self.cam.get(cv2.CAP_PROP_FPS)
        message = f"FPS: {self.fps}"
        self.lbl_status_bar.configure(text=message)
        self.lbl_status_bar.update()

# ------------------ CREATE WIDGETS ---------------------------------------#
    def create_widgets(self):
        """Create widgets"""
        self.main_frame = ttk.Frame(
            self.root,
            relief=tk.RIDGE
        )
        
        # Create canvas to display image
        self.canvas = tk.Canvas(self.main_frame, width=640, height=480)

        message = f" OpenCV Video Stream"
        self.lbl_status_bar = tk.Label(
            self.root, text=message, anchor=tk.W, relief=tk.RIDGE
        )

        BUTTON_WIDTH = 16
        self.btn_start_stop = ttk.Button(
            self.root, text="Start Stream",
            command=self.start_stop_stream,
            width=BUTTON_WIDTH
        )

        self.btn_rotate = ttk.Button(
            self.root,
            text="Rotate",
            command=self.rotate_image
        )
        self.btn_snapshot = ttk.Button(
            self.root, text="Snapshot",
            command=self.snapshot,
            width=BUTTON_WIDTH
        )
        self.btn_quit = ttk.Button(
            self.root, text="Quit", command=self.quit, width=BUTTON_WIDTH)

        self.canvas.grid(row=0, column=0, columnspan=4)

        self.btn_start_stop.grid(row=1, column=0)
        self.btn_rotate.grid(row=1, column=1)
        self.btn_snapshot.grid(row=1, column=2)
        self.btn_quit.grid(row=1, column=3)

        self.lbl_status_bar.grid(row=2, column=0, columnspan=4, sticky="WE")

        # Set padding for all widgets
        for child in self.root.winfo_children():
            child.grid_configure(padx=6, pady=6, ipadx=1, ipady=1)

        # The Escape key will activate the quit method
        self.root.bind('<Escape>', self.quit)

# --------------------------- QUIT PROGRAM --------------------------------#
    def quit(self, *args):
        try:
            # If cam is in use, release it
            if self.cam.isOpened():
                self.cam.release()
        except:
            pass
        self.root.destroy()


video_star = VideoStar()
