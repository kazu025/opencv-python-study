"""
MP4動画をグレースケール化して保存する。

camera_record.mp4 を読み込み、
gray_video.mp4 として保存する。

frame             カラー画像（3チャンネル）
gray_frame        白黒画像（1チャンネル）
gray_bgr_frame    白黒に見える3チャンネル画像

"""

from pathlib import Path

import cv2

# 
base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "images" / "private" / "camera_record.mp4"
output_path = base_dir / "images" / "private" / "gray_video.mp4"

# 動画ファイルが存在するか確認
if not input_path.exists():
    print(f"Error: Input video file does not exist: {input_path}")
    raise SystemExit
# 動画ファイルを開く
capture = cv2.VideoCapture(str(input_path))
# 動画ファイルが正常に開けたか確認
if not capture.isOpened():
    print(f"Error: Could not open the input video: {input_path}")
    raise SystemExit

# 動画のプロパティを取得
fps = capture.get(cv2.CAP_PROP_FPS)     # フレームレート
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # 幅
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 高さ

# 画像を保存するための設定を行う
if fps <= 0:
    fps = 20.0

# VideoWriterオブジェクトを作成
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

    # VideoWriterへ渡すため、3チャンネル画像に戻す
    gray_bgr_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

    writer.write(gray_bgr_frame)
    cv2.imshow("Gray Video", gray_bgr_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
writer.release()
cv2.destroyAllWindows()

print(f"Saved: {output_path}")