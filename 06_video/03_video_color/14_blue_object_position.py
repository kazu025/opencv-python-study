"""
動画の青色物体の位置・大きさ・中心を取得する
  : cv2.inRange()
  : cv2.findContours()
  : cv2.boundingRect()
  : cv2.circle()
"""

from pathlib import Path

import cv2
import numpy as np


video_path = Path(__file__).resolve().parents[2] / "images" / "private" / "sample01.mp4"
capture = cv2.VideoCapture(str(video_path))
if not capture.isOpened():
    print(f"Error: Could not open the video: {video_path}")
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
    mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result = frame.copy()

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue
        x, y, width, height = cv2.boundingRect(contour)
        center = (x + width // 2, y + height // 2)
        cv2.rectangle(result, (x, y), (x + width, y + height), (0, 0, 255), 2)
        cv2.circle(result, center, 6, (0, 0, 255), -1)
        cv2.putText(result, f"center={center}", (x, max(y - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow("Blue Mask", mask)
    cv2.imshow("Blue Object Position", result)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
