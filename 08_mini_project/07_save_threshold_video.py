"""
動画を二値化して保存する。

camera_record.mp4をグレースケール化し、
明るさがthreshold_value以上の部分を白、
それ以外を黒に変換する。
"""

from pathlib import Path

import cv2

# MP4動画のパスを指定
base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "images" / "private" / "camera_record.mp4"
output_path = base_dir / "images" / "private" / "threshold_video.mp4"
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
# 二値化の閾値を設定
threshold_value = 127

while True:
    success, frame = capture.read()

    if not success:
        break
    # グレースケール化
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 二値化
    _, binary_frame = cv2.threshold(
        gray_frame,
        threshold_value,
        255,
        cv2.THRESH_BINARY,
    )
    # VideoWriterへ渡すため、3チャンネル画像に戻す
    binary_bgr_frame = cv2.cvtColor(
        binary_frame,
        cv2.COLOR_GRAY2BGR,
    )

    writer.write(binary_bgr_frame)
    cv2.imshow("Threshold Video", binary_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
writer.release()
cv2.destroyAllWindows()

print(f"Saved: {output_path}")