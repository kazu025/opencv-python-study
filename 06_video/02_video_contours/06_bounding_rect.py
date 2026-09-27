"""
動画の輪郭を外接長方形で囲む
  : cv2.VideoCapture()
  : cv2.findContours()
  : cv2.contourArea()
  : cv2.boundingRect()
  : cv2.rectangle()

処理の流れ
  1. 動画を1フレームずつ読み込む
  2. フレームをグレースケール化して二値化する
  3. 輪郭を検出する
  4. 面積が一定以上の輪郭を選ぶ
  5. 外接長方形の x, y, w, h を取得する
  6. フレーム上に長方形を描画する
  7. 動画の最後、qキー、Escキーで終了する

boundingRect() は、輪郭を囲む水平・垂直な長方形を返す。
  x, y : 長方形の左上の座標
  w, h : 長方形の幅と高さ
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
        cv2.rectangle(
            result_frame,
            (x, y),
            (x + width, y + height),
            (0, 0, 255),
            2,
        )

    cv2.imshow("Original Video", frame)
    cv2.imshow("Binary Video", binary_frame)
    cv2.imshow("Bounding Rectangles", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
