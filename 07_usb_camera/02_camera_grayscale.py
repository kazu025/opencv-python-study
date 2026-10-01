"""
USBカメラの映像をグレースケール化して表示する
  : cv2.VideoCapture()
  : cv2.cvtColor()
  : cv2.imshow()

処理の流れ
  1. USBカメラを開く
  2. カメラから1フレームずつ読み込む
  3. BGRカラー画像をグレースケール画像へ変換する
  4. 元の映像とグレースケール映像を表示する
  5. qキー、Escキーで終了する
"""

import cv2


camera_number = 0
capture = cv2.VideoCapture(camera_number)

if not capture.isOpened():
    print(f"Error: Could not open the camera: {camera_number}")
    raise SystemExit

print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()

    if not ret:
        print("Error: Could not read a frame from the camera.")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Original Camera", frame)
    cv2.imshow("Grayscale Camera", gray_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()