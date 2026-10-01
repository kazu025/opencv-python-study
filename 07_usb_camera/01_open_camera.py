"""
USBカメラの映像を読み込み、リアルタイムに表示する
  : cv2.VideoCapture()
  : capture.read()
  : cv2.imshow()

処理の流れ
  1. USBカメラを開く
  2. カメラから1フレームずつ読み込む
  3. 読み込んだフレームを画面に表示する
  4. qキー、Escキーで終了する

VideoCapture() の引数はカメラ番号を表す。
通常、内蔵カメラや最初に接続されたカメラには0を指定する。
"""

import cv2


camera_number = 0
capture = cv2.VideoCapture(camera_number)

if not capture.isOpened():
    print(f"Error: Could not open the camera: {camera_number}")
    print("Check that a camera is connected and available.")
    raise SystemExit

print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()

    if not ret:
        print("Error: Could not read a frame from the camera.")
        break

    cv2.imshow("USB Camera", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
