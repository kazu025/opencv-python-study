"""
動画内の青色物体を検出し、長方形と中心点を描画して保存する。
"""

from pathlib import Path

import cv2
import numpy as np

# MP4動画のパスを指定
base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "images" / "private" / "camera_record.mp4"
output_path = base_dir / "images" / "private" / "blue_tracking_video.mp4"
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
# VideoWriterオブジェクトを作成
writer = cv2.VideoWriter(
    str(output_path),
    fourcc,
    fps,
    (width, height),
)
# 青色のHSV範囲を定義
lower_blue = np.array([100, 100, 50])
upper_blue = np.array([140, 255, 255])

while True:
    success, frame = capture.read()

    if not success:
        break
    # HSV色空間に変換
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 青色のマスクを作成
    blue_mask = cv2.inRange(
        hsv_frame,
        lower_blue,
        upper_blue,
    )
    # 輪郭を検出
    contours, _ = cv2.findContours(
        blue_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    # VideoWriterへ渡すため、3チャンネル画像に戻す
    result_frame = frame.copy()
    # 輪郭を描画する
    if contours:
        # 最大の輪郭を取得
        contour = max(contours, key=cv2.contourArea)
        # 輪郭の面積が小さい場合は無視する
        if cv2.contourArea(contour) >= 500:
            # 輪郭を囲む長方形を取得
            x, y, box_width, box_height = cv2.boundingRect(contour)
            # 長方形の中心点を計算 
            center_x = x + box_width // 2
            center_y = y + box_height // 2
            # 長方形を描画
            cv2.rectangle(
                result_frame,
                (x, y),
                (x + box_width, y + box_height),
                (0, 255, 0),
                2,
            )
            # 中心点を描画
            cv2.circle(
                result_frame,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1,
            )
            # 青色物体のラベルを描画
            cv2.putText(
                result_frame,
                "Blue object",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

    writer.write(result_frame)
    cv2.imshow("Blue Tracking Video", result_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
writer.release()
cv2.destroyAllWindows()

print(f"Saved: {output_path}")