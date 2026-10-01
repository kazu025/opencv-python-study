"""
USBカメラの映像を二値化して表示する
  : cv2.VideoCapture()
  : cv2.cvtColor()
  : cv2.threshold()
"""

import cv2

# --------------------------------------------------------------------------
# カメラを使う場合
# camera_number = 0
# capture = cv2.VideoCapture(camera_number)
# --------------------------------------------------------------------------
# 動画を使う場合
video_path = r".\images\private\sample01.mp4"
capture = cv2.VideoCapture(video_path)
# --------------------------------------------------------------------------

if not capture.isOpened():
    print(f"Error: Could not open the camera")
    raise SystemExit

threshold_value = 128
print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()

    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, binary_frame = cv2.threshold(
        gray_frame,
        threshold_value,
        255,
        cv2.THRESH_BINARY,
    )

    cv2.imshow("Original Camera", frame)
    cv2.imshow("Binary Camera", binary_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()