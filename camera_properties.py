# https://www.geeksforgeeks.org/how-to-get-properties-of-python-cv2-videocapture-object/

# importing cv2
import cv2

# For tesing Video File
# capture=cv2.VideoCapture("sample.webm")

# For webcam
capture = cv2.VideoCapture(0)
print("Current OpenCV Camera Settings")

# Show values of current camera properties
print(f" CV_CAP_PROP_FRAME_WIDTH: {capture.get(cv2.CAP_PROP_FRAME_WIDTH)}")
print(f"CV_CAP_PROP_FRAME_HEIGHT: {capture.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
print(f"            CAP_PROP_FPS: {capture.get(cv2.CAP_PROP_FPS)}")
print(f"       CAP_PROP_POS_MSEC: {capture.get(cv2.CAP_PROP_POS_MSEC)}")
print(f"    CAP_PROP_FRAME_COUNT: {capture.get(cv2.CAP_PROP_FRAME_COUNT)}")
print(f"     CAP_PROP_BRIGHTNESS: {capture.get(cv2.CAP_PROP_BRIGHTNESS)}")
print(f"       CAP_PROP_CONTRAST: {capture.get(cv2.CAP_PROP_CONTRAST)}")
print(f"     CAP_PROP_SATURATION: {capture.get(cv2.CAP_PROP_SATURATION)}")
print(f"            CAP_PROP_HUE: {capture.get(cv2.CAP_PROP_HUE)}")
print(f"           CAP_PROP_GAIN: {capture.get(cv2.CAP_PROP_GAIN)}")
print(f"    CAP_PROP_CONVERT_RGB: {capture.get(cv2.CAP_PROP_CONVERT_RGB)}")

# Release window
capture.release()
cv2.destroyAllWindows()
