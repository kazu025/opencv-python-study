"""
カメラ映像の青色物体の位置・大きさ・中心を取得する
  : cv2.inRange()
  : cv2.findContours()
  : cv2.boundingRect()
  : cv2.circle()
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
        center_x = x + width // 2
        center_y = y + height // 2

        cv2.rectangle(
            result_frame,
            (x, y),
            (x + width, y + height),
            (0, 0, 255),
            2,
        )

        cv2.circle(
            result_frame,
            (center_x, center_y),
            6,
            (0, 0, 255),
            -1,
        )

        cv2.putText(
            result_frame,
            f"center=({center_x}, {center_y})",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2,
        )

    cv2.imshow("Blue Mask", blue_mask)
    cv2.imshow("Blue Object Position", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()