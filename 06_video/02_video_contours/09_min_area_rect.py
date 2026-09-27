"""
動画の輪郭を回転した最小面積長方形で囲む
  : cv2.minAreaRect()
  : cv2.boxPoints()
  : cv2.drawContours()

処理の流れ
  1. 動画を1フレームずつ読み込む
  2. グレースケール化して二値化する
  3. 輪郭を検出し、面積の小さい輪郭を除外する
  4. minAreaRect() で回転を許した長方形を求める
  5. boxPoints() で4頂点を取得する
  6. 輪郭と回転長方形をフレーム上に描画する
  7. 動画の最後、qキー、Escキーで終了する

boundingRect() は水平・垂直な長方形を返すのに対して、
minAreaRect() は輪郭を最も小さく囲む回転長方形を返す。
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

        # 輪郭を最も小さく囲む回転長方形を計算する
        rect = cv2.minAreaRect(contour)
        # rectから長方形の4つの頂点座標を計算する。
        box = cv2.boxPoints(rect)
        # 整数に変換
        box = np.intp(box)

        cv2.drawContours(result_frame, [box], 0, (0, 255, 0), 2)

    cv2.imshow("Original Video", frame)
    cv2.imshow("Binary Video", binary_frame)
    cv2.imshow("Minimum Area Rectangles", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
