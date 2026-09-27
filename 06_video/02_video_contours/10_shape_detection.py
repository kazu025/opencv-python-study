"""
動画の輪郭を多角形近似し、図形の種類を判定する
  : cv2.approxPolyDP()
  : cv2.minAreaRect()
  : cv2.putText()

処理の流れ
  1. 動画を1フレームずつ読み込む
  2. グレースケール化して反転二値化する
  3. 輪郭を検出し、面積の小さい輪郭を除外する
  4. 輪郭を多角形に近似する
  5. 頂点数と縦横比から図形を判定する
  6. 判定結果をフレーム上に表示する
  7. 動画の最後、qキー、Escキーで終了する

頂点数が3なら三角形、4なら正方形または長方形、
5以上なら円または楕円の候補として判定する。
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
        cv2.THRESH_BINARY_INV,
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

        perimeter = cv2.arcLength(contour, True)
        epsilon = 0.02 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)
        vertices = len(approx)

        (_, _), (width, height), _ = cv2.minAreaRect(contour)
        aspect_ratio = max(width, height) / min(width, height) if min(width, height) > 0 else 0

        if vertices == 3:
            shape_name = "Triangle"
        elif vertices == 4:
            shape_name = "Square" if aspect_ratio < 1.10 else "Rectangle"
        else:
            shape_name = "Circle" if aspect_ratio < 1.10 else "Ellipse"

        x, y, _, _ = cv2.boundingRect(contour)
        cv2.drawContours(result_frame, [approx], -1, (0, 255, 0), 2)
        cv2.putText(
            result_frame,
            shape_name,
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

    cv2.imshow("Original Video", frame)
    cv2.imshow("Binary Video", binary_frame)
    cv2.imshow("Shape Detection", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
