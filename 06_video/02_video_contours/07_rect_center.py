"""
動画の輪郭を外接長方形で囲み、その中心を表示する
  : cv2.boundingRect()
  : cv2.rectangle()
  : cv2.circle()

処理の流れ
  1. 動画を1フレームずつ読み込む
  2. グレースケール化して二値化する
  3. 輪郭を検出し、面積の小さい輪郭を除外する
  4. 外接長方形の座標と大きさを取得する
  5. 長方形の中心座標を計算する
  6. 長方形と中心点をフレーム上に描画する
  7. 動画の最後、qキー、Escキーで終了する

長方形の中心は、次の式で求められる。
  center_x = x + width // 2
  center_y = y + height // 2
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

threshold_value = 128
min_area = 500
print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()

    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary_frame = cv2.threshold(
        gray_frame,
        threshold_value,
        255,
        cv2.THRESH_BINARY,
    )

    contours, _ = cv2.findContours(
        binary_frame,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    result_frame = frame.copy()

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < min_area:
            continue

        x, y, width, height = cv2.boundingRect(contour)
        center_x = x + width // 2
        center_y = y + height // 2

        cv2.rectangle(
            result_frame,
            (x, y),
            (x + width, y + height),
            (0, 0, 255),
            2,
        )
        cv2.circle(
            result_frame,
            (center_x, center_y),
            6,
            (255, 0, 0),
            -1,
        )

    cv2.imshow("Original Video", frame)
    cv2.imshow("Binary Video", binary_frame)
    cv2.imshow("Centers", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
