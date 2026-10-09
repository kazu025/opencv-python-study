"""
青色物体を検出し、中心点の移動軌跡を描画して保存する。
"""

from collections import deque
from pathlib import Path

import cv2
import numpy as np


base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "images" / "private" / "camera_record.mp4"
output_path = base_dir / "images" / "private" / "tracking_trail_video.mp4"

capture = cv2.VideoCapture(str(input_path))

if not capture.isOpened():
    print("Error: Could not open the input video.")
    raise SystemExit

fps = capture.get(cv2.CAP_PROP_FPS)
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

if fps <= 0:
    fps = 20.0

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(
    str(output_path),
    fourcc,
    fps,
    (width, height),
)
# 青色のHSV範囲を定義
lower_blue = np.array([100, 100, 50])
upper_blue = np.array([140, 255, 255])
# 中心点の移動軌跡を保存するためのdequeを作成
trail = deque(maxlen=50)

while True:
    success, frame = capture.read()

    if not success:
        break
    # HSV色空間に変換
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    # 輪郭を検出
    contours, _ = cv2.findContours(
        blue_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    # VideoWriterへ渡すため、3チャンネル画像に戻す
    result_frame = frame.copy()
    # 青色物体が検出された場合、最大の輪郭を取得し、中心点を計算して移動軌跡を描画
    if contours:
        # 最大の輪郭を取得
        contour = max(contours, key=cv2.contourArea)
        # 輪郭の面積が小さい場合は無視する
        if cv2.contourArea(contour) >= 500:
            # 輪郭を囲む長方形を取得
            x, y, box_width, box_height = cv2.boundingRect(contour)
            # 中心点を計算
            center = (
                x + box_width // 2,
                y + box_height // 2,
            )
            # 中心点を描画
            trail.append(center)
            # 長方形を描画
            cv2.rectangle(
                result_frame,
                (x, y),
                (x + box_width, y + box_height),
                (0, 255, 0),
                2,
            )
    # 移動軌跡を描画
    if len(trail) >= 2:
        points = np.array(trail, dtype=np.int32)
        cv2.polylines(
            result_frame,
            [points],
            False,
            (0, 0, 255),
            2,
        )

    writer.write(result_frame)
    cv2.imshow("Tracking Trail Video", result_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
writer.release()
cv2.destroyAllWindows()

print(f"Saved: {output_path}")