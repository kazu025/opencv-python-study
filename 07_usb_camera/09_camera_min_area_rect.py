"""
カメラ映像の輪郭を回転長方形で囲む
  : cv2.minAreaRect()
  : cv2.boxPoints()
  : cv2.drawContours()
"""

from pathlib import Path

import cv2
import numpy as np


camera_number = 0
capture = cv2.VideoCapture(camera_number)

if not capture.isOpened():
    print(f"Error: Could not open the camera: {camera_number}")
    raise SystemExit

threshold_value = 128
min_area = 500

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

    contours, _ = cv2.findContours(
        binary_frame,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    result_frame = frame.copy()

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < min_area:
            continue

        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)

        cv2.drawContours(
            result_frame,
            [box],
            0,
            (0, 255, 0),
            2,
        )

    cv2.imshow("Camera", frame)
    cv2.imshow("Binary Camera", binary_frame)
    cv2.imshow("Minimum Area Rectangles", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()