"""
カメラ映像の輪郭を囲み、外接長方形の中心を表示する
  : cv2.boundingRect()
  : cv2.rectangle()
  : cv2.circle()
"""

import cv2


camera_number = 0
capture = cv2.VideoCapture(camera_number)

if not capture.isOpened():
    print(f"Error: Could not open the camera: {camera_number}")
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

    cv2.imshow("Camera", frame)
    cv2.imshow("Binary Camera", binary_frame)
    cv2.imshow("Centers", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
