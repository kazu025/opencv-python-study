"""
動画の輪郭の重心を求め、外接長方形の中心と比較する
  : cv2.moments()
  : cv2.boundingRect()
  : cv2.rectangle()
  : cv2.circle()

処理の流れ
  1. 動画を1フレームずつ読み込む
  2. グレースケール化して二値化する
  3. 輪郭を検出し、面積の小さい輪郭を除外する
  4. 外接長方形の中心を計算する
  5. moments() から輪郭の重心を計算する
  6. 2種類の中心をフレーム上に描画する
  7. 動画の最後、qキー、Escキーで終了する

外接長方形の中心は長方形の中心であり、
輪郭の重心は輪郭の形や面積の分布から求めた中心である。
"""

from pathlib import Path

import cv2


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

        x, y, width, height = cv2.boundingRect(contour)
        rect_center = (x + width // 2, y + height // 2)

        moments = cv2.moments(contour)
        if moments["m00"] == 0:
            continue

        centroid = (
            int(moments["m10"] / moments["m00"]),
            int(moments["m01"] / moments["m00"]),
        )

        cv2.rectangle(
            result_frame,
            (x, y),
            (x + width, y + height),
            (0, 0, 255),
            2,
        )
        cv2.circle(result_frame, rect_center, 6, (255, 0, 0), -1)
        cv2.circle(result_frame, centroid, 6, (0, 255, 0), -1)

    cv2.imshow("Original Video", frame)
    cv2.imshow("Binary Video", binary_frame)
    cv2.imshow("Centroids", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
