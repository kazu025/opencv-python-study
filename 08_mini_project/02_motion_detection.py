"""
カメラ映像から動いている物体を検出する
  : cv2.createBackgroundSubtractorMOG2()
  : cv2.findContours()
  : cv2.boundingRect()
"""

import cv2

camera_number = 0
capture = cv2.VideoCapture(camera_number)

if not capture.isOpened():
    print(f"Error: Could not open the camera: {camera_number}")
    raise SystemExit

# 背景差分法のための背景差分器を作成
# MOG2は、混合ガウスモデルを使用して背景を学習するアルゴリズムです。
background_subtractor = cv2.createBackgroundSubtractorMOG2()
min_area = 1000

print("Press q or Esc to quit.")

while True:
    ret, frame = capture.read()

    if not ret:
        break
    # 背景差分を適用して、動いている物体のマスク画像を取得
    # 動いている物体は白く、それ以外は黒くなる。
    # 判定が不確かな場合は、グレーになる。
    motion_mask = background_subtractor.apply(frame)
    # グレーの部分を白くするために、二値化を行う
    _, motion_mask = cv2.threshold(
        motion_mask,
        200,
        255,
        cv2.THRESH_BINARY,
    )
    # 白い部分を使って、輪郭を検出
    contours, _ = cv2.findContours(
        motion_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    # 元のフレームをコピーして、描画用のフレームを作成
    result_frame = frame.copy()

    for contour in contours:
        # 面積がmin_area以上の輪郭を抽出
        area = cv2.contourArea(contour)
        if area < min_area:
            continue
        # 輪郭の外接長方形を取得
        x, y, width, height = cv2.boundingRect(contour)
        # 外接長方形を描画
        cv2.rectangle(
            result_frame,
            (x, y),
            (x + width, y + height),
            (0, 0, 255),
            2,
        )
        # 検出した物体のラベルを描画
        cv2.putText(
            result_frame,
            "Motion",
            (x, max(y - 10, 20)), # y座標が負にならないようにする
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

    cv2.imshow("Motion Mask", motion_mask)
    cv2.imshow("Motion Detection", result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

capture.release()
cv2.destroyAllWindows()
