"""
動画の各フレームをグレースケールに変換する
  : cv2.VideoCapture()
  : cv2.cvtColor()
  : cv2.imshow()

処理の流れ
  1. 動画ファイルを開く
  2. 1フレームずつ読み込む
  3. BGRカラー画像をグレースケール画像へ変換する
  4. 元のフレームとグレースケール画像を表示する
  5. 動画の最後、qキー、Escキーで終了する

動画は連続した静止画像（フレーム）で構成されているため、
静止画と同じ画像処理をフレームごとに適用できる。
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

print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()

    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Original Video", frame)
    cv2.imshow("Grayscale Video", gray_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
