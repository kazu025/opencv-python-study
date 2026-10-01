"""
カメラ映像からHSVで青色の物体を検出する
  : cv2.cvtColor()
  : cv2.inRange()
  : cv2.findContours()
  : cv2.boundingRect()
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
min_area = 500

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

    contours, _ = cv2.findContours(
        blue_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    result_frame = frame.copy()

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < min_area:
            continue

        x, y, width, height = cv2.boundingRect(contour)

        cv2.rectangle(
            result_frame,
            (x, y),
            (x + width, y + height),
            (0, 0, 255),
            2,
        )

    cv2.imshow("Camera", frame)
    cv2.imshow("Blue Mask", blue_mask)
    cv2.imshow("Blue Only", blue_only)
    cv2.imshow("Blue Detection", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()