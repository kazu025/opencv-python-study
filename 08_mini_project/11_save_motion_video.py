"""
動画内の動きを検出し、長方形で囲んで保存する。
"""

from pathlib import Path

import cv2


base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "images" / "private" / "camera_record.mp4"
output_path = base_dir / "images" / "private" / "motion_video.mp4"

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
# 動き検出のための背景差分法を使用する
background_subtractor = cv2.createBackgroundSubtractorMOG2()

while True:
    success, frame = capture.read()

    if not success:
        break
    # 動き検出のためのマスクを作成
    motion_mask = background_subtractor.apply(frame)
    # 二値化して動きのある部分を強調
    _, motion_mask = cv2.threshold(
        motion_mask,
        200,
        255,
        cv2.THRESH_BINARY,
    )
    # 輪郭を検出
    contours, _ = cv2.findContours(
        motion_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    result_frame = frame.copy()

    for contour in contours:
        # 輪郭の面積が小さい場合は無視する
        if cv2.contourArea(contour) < 500:
            continue
        # 輪郭を囲む長方形を取得
        x, y, box_width, box_height = cv2.boundingRect(contour)
        # 長方形を描画
        cv2.rectangle(
            result_frame,
            (x, y),
            (x + box_width, y + box_height),
            (0, 0, 255),
            2,
        )
        # 動きが検出されたことを示すラベルを描画
        cv2.putText(
            result_frame,
            "Motion",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

    writer.write(result_frame)
    cv2.imshow("Motion Video", result_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
writer.release()
cv2.destroyAllWindows()

print(f"Saved: {output_path}")