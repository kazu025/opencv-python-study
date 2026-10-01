"""
動画の各フレームから輪郭を検出する
  : cv2.VideoCapture()
  : cv2.cvtColor()
  : cv2.threshold()
  : cv2.findContours()
  : cv2.drawContours()
"""

import cv2


camera_number = 0
capture = cv2.VideoCapture(camera_number)

if not capture.isOpened():
    print(f"Error: Could not open the camera: {camera_number}")
    raise SystemExit

threshold_value = 128
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
    cv2.drawContours(
        result_frame,
        contours,
        -1,
        (0, 255, 0),
        2,
    )

    cv2.imshow("Original Video", frame)
    cv2.imshow("Binary Video", binary_frame)
    cv2.imshow("Contours", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()