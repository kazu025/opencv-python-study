"""
動画からエッジを検出して保存する。

Cannyエッジ検出によって、
明るさが急に変化する境界部分を表示・保存する。
"""

from pathlib import Path

import cv2

# MP4動画のパスを指定
base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "images" / "private" / "camera_record.mp4"
output_path = base_dir / "images" / "private" / "edge_video.mp4"
# 動画ファイルが存在するか確認
if not input_path.exists(): 
    print(f"Error: Input video file does not exist: {input_path}")
    raise SystemExit
# 動画ファイルを開く
capture = cv2.VideoCapture(str(input_path))
# 動画ファイルが正常に開けたか確認
if not capture.isOpened():
    print("Error: Could not open the input video.")
    raise SystemExit
# 動画のプロパティを取得
fps = capture.get(cv2.CAP_PROP_FPS)
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

if fps <= 0:
    fps = 20.0
# 画像を保存するための設定を行う
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(
    str(output_path),
    fourcc,
    fps,
    (width, height),
)

while True:
    success, frame = capture.read()

    if not success:
        break
    # グレースケール化
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Cannyエッジ検出
    edge_frame = cv2.Canny(
        gray_frame,
        50,
        150,
    )
    # VideoWriterへ渡すため、3チャンネル画像に戻す
    edge_bgr_frame = cv2.cvtColor(
        edge_frame,
        cv2.COLOR_GRAY2BGR,
    )
    # 保存するフレームを書き込む
    writer.write(edge_bgr_frame)
    cv2.imshow("Edge Video", edge_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
writer.release()
cv2.destroyAllWindows()

print(f"Saved: {output_path}")