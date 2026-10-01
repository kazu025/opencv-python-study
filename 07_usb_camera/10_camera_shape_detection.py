"""
カメラ映像の輪郭を図形として判定する
  : cv2.approxPolyDP()
  : cv2.minAreaRect()
  : cv2.putText()
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

        if min(width, height) > 0:
            aspect_ratio = max(width, height) / min(width, height)
        else:
            aspect_ratio = 0

        if vertices == 3:
            shape_name = "Triangle"
        elif vertices == 4:
            if aspect_ratio < 1.10:
                shape_name = "Square"
            else:
                shape_name = "Rectangle"
        else:
            if aspect_ratio < 1.10:
                shape_name = "Circle"
            else:
                shape_name = "Ellipse"

        x, y, _, _ = cv2.boundingRect(contour)

        cv2.drawContours(
            result_frame,
            [approx],
            -1,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            result_frame,
            shape_name,
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

    cv2.imshow("Camera", frame)
    cv2.imshow("Binary Camera", binary_frame)
    cv2.imshow("Shape Detection", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()