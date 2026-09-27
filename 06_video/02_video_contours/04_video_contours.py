"""
動画の各フレームから輪郭を検出する
  : cv2.VideoCapture()
  : cv2.cvtColor()
  : cv2.threshold()
  : cv2.findContours()
  : cv2.drawContours()

処理の流れ
  1. 動画ファイルを開く
  2. 1フレームずつ読み込む
  3. グレースケール化して二値化する
  4. 二値画像から外側の輪郭を検出する
  5. 検出した輪郭を元のフレームに描画する
  6. 動画の最後、qキー、Escキーで終了する

findContours() は白い領域の境界を検出するため、
二値画像では検出したい対象物を白くする。
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
    cv2.drawContours(result_frame, contours, -1, (0, 255, 0), 2)

    cv2.imshow("Original Video", frame)
    cv2.imshow("Binary Video", binary_frame)
    cv2.imshow("Contours", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
