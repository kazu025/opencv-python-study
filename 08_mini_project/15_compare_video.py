"""
元のカラー映像とグレースケール映像を
左右に並べて保存する。
"""

from pathlib import Path

import cv2


base_dir = Path(__file__).resolve().parents[1]
input_path = base_dir / "images" / "private" / "camera_record.mp4"
output_path = base_dir / "images" / "private" / "compare_video.mp4"

capture = cv2.VideoCapture(str(input_path))

if not capture.isOpened():
    print("Error: Could not open the input video.")
    raise SystemExit

fps = capture.get(cv2.CAP_PROP_FPS)
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

if fps <= 0:
    fps = 20.0

compare_width = width * 2

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(
    str(output_path),
    fourcc,
    fps,
    (compare_width, height),
)

while True:
    success, frame = capture.read()

    if not success:
        break

    gray_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY,
    )

    gray_bgr_frame = cv2.cvtColor(
        gray_frame,
        cv2.COLOR_GRAY2BGR,
    )

    compare_frame = cv2.hconcat(
        [frame, gray_bgr_frame]
    )

    cv2.putText(
        compare_frame,
        "Original",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )

    cv2.putText(
        compare_frame,
        "Grayscale",
        (width + 20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )

    writer.write(compare_frame)
    cv2.imshow("Compare Video", compare_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()
writer.release()
cv2.destroyAllWindows()

print(f"Saved: {output_path}")