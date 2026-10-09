"""
動画にフレーム番号と経過時間を表示して保存する。
"""

from pathlib import Path

import cv2


base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "images" / "private" / "camera_record.mp4"
output_path = base_dir / "images" / "private" / "video_info.mp4"

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

frame_number = 0

while True:
    success, frame = capture.read()

    if not success:
        break
    # フレーム番号と経過時間を計算
    elapsed_seconds = frame_number / fps
    # フレーム番号を表示
    cv2.putText(
        frame,
        f"Frame: {frame_number}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )
    # 経過時間を表示
    cv2.putText(
        frame,
        f"Time: {elapsed_seconds:.2f} sec",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )

    writer.write(frame)
    cv2.imshow("Video Info", frame)

    frame_number += 1

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
writer.release()
cv2.destroyAllWindows()

print(f"Saved: {output_path}")
