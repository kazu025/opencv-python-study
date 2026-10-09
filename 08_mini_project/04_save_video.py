"""
カメラ映像をMP4ファイルに保存する。

カメラから読み込んだフレームを表示しながら、
images/private/camera_record.mp4 に保存する。
qキーで終了する。
"""

from pathlib import Path

import cv2


output_path = (
    Path(__file__).resolve().parents[1]
    / "images"
    / "private"
    / "camera_record.mp4"
)

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    print("Error: Could not open the camera.")
    raise SystemExit

fps = 20.0
# 画面サイズを取得
# カメラが対応している初期サイズを取得するために、
# CAP_PROP_FRAME_WIDTH と CAP_PROP_FRAME_HEIGHT を使用する
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

#　画像を保存するための設定を行う
# mp4vは、MPEG-4 Part 2のビデオコーデックを使用するためのfourccコードです。
# MP4形式の動画を保存する場合に使用されます。
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# VideoWriterオブジェクトを作成
writer = cv2.VideoWriter(
    str(output_path),   # 保存するファイルパス
    fourcc,             # 圧縮方式(ビデオコーデック)
    fps,                # フレームレート
    (width, height),    # フレームサイズ
)

while True:
    success, frame = capture.read()

    if not success:
        print("Error: Could not read a frame.")
        break

    # 保存するフレームを書き込む
    writer.write(frame)
    cv2.imshow("Save Video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
writer.release()
cv2.destroyAllWindows()

print(f"Saved: {output_path}")