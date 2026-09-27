"""
動画の各フレームを二値化する
  : cv2.VideoCapture()
  : cv2.cvtColor()
  : cv2.threshold()
  : cv2.imshow()

処理の流れ
  1. 動画ファイルを開く
  2. 1フレームずつ読み込む
  3. BGRカラー画像をグレースケール画像へ変換する
  4. しきい値を使って二値画像へ変換する
  5. 元のフレームと二値画像を表示する
  6. 動画の最後、qキー、Escキーで終了する

二値化では、画素の明るさがしきい値以上なら255（白）、
しきい値未満なら0（黒）に変換する。
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
    _, binary_frame = cv2.threshold( # _ :実際に使われた閾値
        gray_frame,
        threshold_value,    # 白黒を分ける基準
        255,                # 白にする画素値
        cv2.THRESH_BINARY,
    )

    cv2.imshow("Original Video", frame)
    cv2.imshow("Binary Video", binary_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
