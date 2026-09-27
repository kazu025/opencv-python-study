"""
動画の複数色の物体を検出し、中心座標を表示する
  : cv2.inRange()
  : cv2.findContours()
  : cv2.boundingRect()
  : cv2.circle()
  : cv2.putText()
"""

from pathlib import Path

import cv2
import numpy as np


video_path = Path(__file__).resolve().parents[2] / "images" / "private" / "sample01.mp4"
capture = cv2.VideoCapture(str(video_path))
if not capture.isOpened():
    print(f"Error: Could not open the video: {video_path}")
    raise SystemExit

color_ranges = {
    "Red": (np.array([0, 100, 100]), np.array([10, 255, 255]), (0, 0, 255)),
    "Green": (np.array([50, 100, 100]), np.array([80, 255, 255]), (0, 255, 0)),
    "Blue": (np.array([100, 100, 100]), np.array([140, 255, 255]), (255, 0, 0)),
    "Yellow": (np.array([20, 100, 100]), np.array([40, 255, 255]), (0, 255, 255)),
}
min_area = 500
print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()
    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    result = frame.copy()

    for name, (lower, upper, color) in color_ranges.items():
        mask = cv2.inRange(hsv_frame, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < min_area:
                continue
            x, y, width, height = cv2.boundingRect(contour)
            center = (x + width // 2, y + height // 2)
            cv2.rectangle(result, (x, y), (x + width, y + height), color, 2)
            cv2.circle(result, center, 6, color, -1)
            cv2.putText(result, f"{name} {center}", (x, max(y - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Multi Color Centers", result)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
