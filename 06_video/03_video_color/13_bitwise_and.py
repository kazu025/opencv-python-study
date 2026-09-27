"""
HSVマスクを使って、動画から青色部分だけをカラー抽出する
  : cv2.inRange()
  : cv2.bitwise_and()
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
print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()
    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    blue_only = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Original Video", frame)
    cv2.imshow("Blue Mask", mask)
    cv2.imshow("Blue Only", blue_only)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
