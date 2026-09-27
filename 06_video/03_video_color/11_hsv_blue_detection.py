"""
動画からHSV色空間を使って青色の領域を検出する
  : cv2.cvtColor()
  : cv2.inRange()
  : cv2.bitwise_and()
  : cv2.findContours()
  : cv2.boundingRect()

処理の流れ
  1. 動画を1フレームずつ読み込む
  2. BGR画像をHSV画像へ変換する
  3. 青色のHSV範囲からマスクを作る
  4. マスクを使って青色部分だけを抽出する
  5. 青色領域の輪郭を検出し、外接長方形を描画する
  6. 動画の最後、qキー、Escキーで終了する

OpenCVのHSVでは、色相Hは0〜179、彩度Sと明度Vは0〜255で表される。
"""

from pathlib import Path

import cv2
import numpy as np


video_path = (
    Path(__file__).resolve().parents[2]
    / "images"
    / "private"
    / "sample01.mp4"
)

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
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    blue_only = cv2.bitwise_and(frame, frame, mask=blue_mask)

    contours, _ = cv2.findContours(
        blue_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    result_frame = frame.copy()

    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue

        x, y, width, height = cv2.boundingRect(contour)
        cv2.rectangle(
            result_frame,
            (x, y),
            (x + width, y + height),
            (0, 0, 255),
            2,
        )

    cv2.imshow("Original Video", frame)
    cv2.imshow("Blue Mask", blue_mask)
    cv2.imshow("Blue Only", blue_only)
    cv2.imshow("Blue Detection", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
