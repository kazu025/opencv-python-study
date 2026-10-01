"""
カメラ映像の輪郭を面積で選別する
  : cv2.findContours()
  : cv2.contourArea()
  : cv2.drawContours()
"""

import cv2
# カメラの番号を指定
camera_number = 0
capture = cv2.VideoCapture(camera_number)
# カメラが開けなかった場合はエラーを出して終了
if not capture.isOpened():
    print(f"Error: Could not open the camera: {camera_number}")
    raise SystemExit

# 2値の閾値
threshold_value = 128
# 面積の閾値
min_area = 500

print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()

    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 2値化
    _, binary_frame = cv2.threshold(
        gray_frame,
        threshold_value,
        255,
        cv2.THRESH_BINARY,
    )
    # 輪郭を検出
    # cv2.findContours()の戻り値はOpenCVのバージョンによって異なる
    # OpenCV 4.xでは、戻り値は contours, hierarchy の2つ   
    # contours: 検出された輪郭のリスト(座標)
    # hierarchy: 輪郭の階層構造
    contours, _ = cv2.findContours(
        binary_frame,
        cv2.RETR_EXTERNAL,      # 輪郭の検出モード:白い領域の外側の輪郭のみを検出
        cv2.CHAIN_APPROX_SIMPLE, # 一番外側の輪郭の座標を簡略化して取得
    )

    result_frame = frame.copy()
    # 輪郭の面積を計算して、指定した面積以上の輪郭のみを描画
    for contour in contours:
        area = cv2.contourArea(contour)

        if area < min_area:
            continue
        # 輪郭を描画
        cv2.drawContours(
            result_frame,
            [contour],
            -1,
            (0, 255, 0),
            2,
        )

    cv2.imshow("Camera", frame)
    cv2.imshow("Binary Camera", binary_frame)
    cv2.imshow("Large Contours", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()