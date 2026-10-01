"""
カメラ映像の複数色の物体を検出し、中心座標を表示する
  : cv2.inRange()
  : cv2.findContours()
  : cv2.boundingRect()
  : cv2.circle()
  : cv2.putText()
"""

import cv2
import numpy as np


camera_number = 0
capture = cv2.VideoCapture(camera_number)

if not capture.isOpened():
    print(f"Error: Could not open the camera: {camera_number}")
    raise SystemExit

color_ranges = {
    "Red": (
        np.array([0, 100, 100]),
        np.array([10, 255, 255]),
        (0, 0, 255),
    ),
    "Green": (
        np.array([50, 100, 100]),
        np.array([80, 255, 255]),
        (0, 255, 0),
    ),
    "Blue": (
        np.array([100, 100, 100]),
        np.array([140, 255, 255]),
        (255, 0, 0),
    ),
    "Yellow": (
        np.array([20, 100, 100]),
        np.array([40, 255, 255]),
        (0, 255, 255),
    ),
}

min_area = 500
print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()

    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    result_frame = frame.copy()

    for color_name, (lower, upper, draw_color) in color_ranges.items():
        mask = cv2.inRange(
            hsv_frame,
            lower,
            upper,
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

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
                draw_color,
                2,
            )

            cv2.circle(
                result_frame,
                (center_x, center_y),
                6,
                draw_color,
                -1,
            )

            cv2.putText(
                result_frame,
                f"{color_name} ({center_x}, {center_y})",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                draw_color,
                2,
            )

    cv2.imshow("Multi Color Centers", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()