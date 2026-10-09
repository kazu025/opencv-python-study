"""
保存したMP4動画を読み込んで再生する。

images/private/camera_record.mp4 を1フレームずつ読み込み、
画面に表示する。
qキーまたはEscキーで終了する。
"""

from pathlib import Path

import cv2

# MP4動画のパスを指定
video_path = (
    Path(__file__).resolve().parents[1]
    / "images"
    / "private"
    / "camera_record.mp4"
)
# 動画ファイルが存在するか確認
if not video_path.exists():
    print(f"Error: Video file does not exist: {video_path}")
    raise SystemExit

# 動画ファイルを開く
capture = cv2.VideoCapture(str(video_path))

# 動画ファイルが正常に開けたか確認
if not capture.isOpened():
    print(f"Error: Could not open video: {video_path}")
    raise SystemExit

while True:
    success, frame = capture.read()

    if not success:
        break

    cv2.imshow("Play Video", frame)
    # 30ミリ秒待機して、キー入力を取得
    # 数値を大きくすると、動画の再生速度が遅くなる
    # 小さくすると、動画の再生速度が速くなる
    key = cv2.waitKey(30) & 0xFF

    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
