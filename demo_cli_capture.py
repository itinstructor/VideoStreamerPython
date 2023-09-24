import cv2

def start_video_capture():
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        cv2.imshow('Video Stream', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            video_capture.release()
            cv2.destroyAllWindows()
            return

    video_capture.release()
    cv2.destroyAllWindows()

while True:
    print("Press 's' to start video capture, 'q' to quit:")
    user_input = input()

    if user_input == 's':
        start_video_capture()
    elif user_input == 'q':
        break
