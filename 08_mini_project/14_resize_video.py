"""
動画の解像度を半分に縮小して保存する。
"""

from pathlib import Path

import cv2


base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "images" / "private" / "camera_record.mp4"
output_path = base_dir / "images" / "private" / "small_video.mp4"

capture = cv2.VideoCapture(str(input_path))

if not capture.isOpened():
    print("Error: Could not open the input video.")
    raise SystemExit

fps = capture.get(cv2.CAP_PROP_FPS)
original_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

if fps <= 0:
    fps = 20.0

width = original_width // 2
height = original_height // 2

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

    resized_frame = cv2.resize(
        frame,
        (width, height),
    )

    writer.write(resized_frame)
    cv2.imshow("Resized Video", resized_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
writer.release()
cv2.destroyAllWindows()

print(f"Saved: {output_path}")