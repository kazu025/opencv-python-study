"""
HSVマスクを使って、カメラ映像から青色部分だけを抽出する
  : cv2.inRange()
  : cv2.bitwise_and()
"""

import cv2
import numpy as np


camera_number = 0
capture = cv2.VideoCapture(camera_number)

if not capture.isOpened():
    print(f"Error: Could not open the camera: {camera_number}")
    raise SystemExit

lower_blue = np.array([100, 100, 100])
upper_blue = np.array([140, 255, 255])

print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()

    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_mask = cv2.inRange(
        hsv_frame,
        lower_blue,
        upper_blue,
    )

    blue_only = cv2.bitwise_and(
        frame,
        frame,
        mask=blue_mask,
    )

    cv2.imshow("Camera", frame)
    cv2.imshow("Blue Mask", blue_mask)
    cv2.imshow("Blue Only", blue_only)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()