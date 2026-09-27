"""
動画ファイルを読み込み、フレームを順番に表示する
  : cv2.VideoCapture()
  : capture.get()
  : capture.read()
  : cv2.imshow()

処理の流れ
  1. 動画ファイルを開く
  2. FPS、フレーム数、幅、高さを取得する
  3. 1フレームずつ読み込む
  4. 読み込んだフレームを画面に表示する
  5. 動画の最後、qキー、Escキーで終了する

動画は連続した静止画像（フレーム）で構成されている。
FPSは1秒間に表示するフレーム数を表す。
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
# 動画の基本情報を取得する
# capture.get()は、情報を取得する関数。引数によりどんな情報を取得するかを指定する。
# 1秒当たりのフレーム数を取得する。
fps = capture.get(cv2.CAP_PROP_FPS)
# 動画全体のフレーム数を取得する
frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
# 動画1フレームの横幅、高さを取得する。
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"video: {video_path}")
print(f"size: {width} x {height}")
print(f"fps: {fps:.2f}")
print(f"frames: {frame_count}")
print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()

    if not ret:
        break

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
