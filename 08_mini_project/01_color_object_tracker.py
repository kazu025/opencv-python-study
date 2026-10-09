"""
青色の物体を検出して追跡する
  : cv2.VideoCapture()
  : cv2.inRange()
  : cv2.findContours()
  : cv2.boundingRect()
  : cv2.circle()
  : cv2.polylines()

青色物体の外接長方形、中心座標、移動軌跡を表示する。
"""

from collections import deque

import cv2
import numpy as np


camera_number = 0
capture = cv2.VideoCapture(camera_number)

if not capture.isOpened():
    print(f"Error: Could not open the camera: {camera_number}")
    raise SystemExit

lower_blue = np.array([100, 100, 100])
upper_blue = np.array([140, 255, 255])
min_area = 500
# 移動軌跡を保存するためのdequeを作成
trail = deque(maxlen=50)

print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()

    if not ret:
        break
    # BGRからHSVに変換
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 青色のマスクを作成
    # 青色を白く、それ以外を黒くしたマスク画像
    blue_mask = cv2.inRange(
        hsv_frame,
        lower_blue,
        upper_blue,
    )

    # 白い部分を使って、輪郭を検出
    contours, _ = cv2.findContours(
        blue_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    # 元のフレームをコピーして、描画用のフレームを作成
    result_frame = frame.copy()
    # 面積がmin_area以上の輪郭を抽出
    large_contours = [
        contour
        for contour in contours
        if cv2.contourArea(contour) >= min_area
    ]

    if large_contours:
        # large_contoursの中で最大の輪郭を取得
        contour = max(large_contours, key=cv2.contourArea)
        # 輪郭の外接長方形を取得
        x, y, width, height = cv2.boundingRect(contour)
        center = (
            x + width // 2,
            y + height // 2,
        )
        # 中心座標をtrailに追加
        trail.append(center)
        # 外接長方形、中心座標を描画
        cv2.rectangle(
            result_frame,
            (x, y),
            (x + width, y + height),
            (0, 0, 255),
            2,
        )
        # 中心座標を描画
        cv2.circle(
            result_frame,
            center,
            6,
            (0, 0, 255),
            -1,
        )
        # 中心座標を表示
        cv2.putText(
            result_frame,
            f"center={center}",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
    # 移動軌跡を描画
    if len(trail) >= 2:
        # trailの座標をnumpy配列に変換
        points = np.array(trail, dtype=np.int32)
        # pointsを使って、移動軌跡を描画
        cv2.polylines(
            result_frame,
            [points],
            False,
            (255, 0, 0),
            2,
        )
    # 結果を表示
    cv2.imshow("Blue Mask", blue_mask)
    cv2.imshow("Color Object Tracker", result_frame)
    # キー入力を待機
    key = cv2.waitKey(1) & 0xFF
    # qまたはEscキーが押されたら終了
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()