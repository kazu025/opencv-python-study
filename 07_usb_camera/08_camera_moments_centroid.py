"""
カメラ映像の輪郭の重心を表示する
  : cv2.moments()
  : cv2.boundingRect()
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

        moments = cv2.moments(contour)

        if moments["m00"] == 0:
            continue

        centroid_x = int(moments["m10"] / moments["m00"])
        centroid_y = int(moments["m01"] / moments["m00"])

        cv2.circle(
            result_frame,
            (centroid_x, centroid_y),
            6,
            (0, 255, 0),
            -1,
        )

    cv2.imshow("Camera", frame)
    cv2.imshow("Binary Camera", binary_frame)
    cv2.imshow("Centroids", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()