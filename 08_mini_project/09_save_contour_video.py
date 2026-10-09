"""
動画から輪郭を検出し、長方形で囲んで保存する。
"""

from pathlib import Path

import cv2


base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "images" / "private" / "camera_record.mp4"
output_path = base_dir / "images" / "private" / "contour_video.mp4"

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

while True:
    success, frame = capture.read()

    if not success:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 二値化
    _, binary_frame = cv2.threshold(
        gray_frame,
        127,
        255,
        cv2.THRESH_BINARY,
    )
    # VideoWriterへ渡すため、3チャンネル画像に戻す
    contours, _ = cv2.findContours(
        binary_frame,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    # VideoWriterへ渡すため、3チャンネル画像に戻す
    result_frame = frame.copy()
    # 輪郭を描画する
    for contour in contours:
        # 輪郭の面積が小さい場合は無視する
        if cv2.contourArea(contour) < 500:
            continue
        # 輪郭を囲む長方形を取得する
        x, y, box_width, box_height = cv2.boundingRect(contour)
        # 長方形を描画する
        cv2.rectangle(
            result_frame,
            (x, y),
            (x + box_width, y + box_height),
            (0, 255, 0),
            2,
        )
    # 保存するフレームを書き込む
    writer.write(result_frame)
    # 表示する
    cv2.imshow("Contour Video", result_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
writer.release()
cv2.destroyAllWindows()

print(f"Saved: {output_path}")