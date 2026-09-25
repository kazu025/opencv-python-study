'''
HSVマスクを使って、複数色の物体を検出する
  : cv2.cvtColor()
  : cv2.inRange()
  : cv2.findContours()
  : cv2.boundingRect()
  : cv2.putText()

処理の流れ
  1. テスト用のカラー画像を作る
  2. BGR画像をHSV画像へ変換する
  3. 検出したい色ごとにHSV範囲を定義する
  4. 色ごとにinRange()でmaskを作る
  5. maskから輪郭を検出する
  6. 色名・外接長方形・中心点を描画する

検出対象
  Red
  Green
  Blue
  Yellow
'''

import cv2
import numpy as  np

# -------------------------------------------------------------------
# テスト画像を作成
# -------------------------------------------------------------------
image = np.ones(
    (600, 800, 3),
    dtype = np.uint8
) * 255

# 赤い四角
cv2.rectangle(image,
              (50, 50),
              (300, 200),
              (0, 0, 255),
              -1
)

# 緑の円
cv2.circle(image,
           (550, 150),
           100,
           (0,255,0),
           -1
)

# 青い四角形
cv2.rectangle(image,
              (80, 350),
              (350, 520),
              (255,0,0),
              -1
)

# 黄色の円
cv2.circle(image,
           (600, 420),
           100,
           (0, 255,255),
           -1
)

# -------------------------------------------------------------------
# BGR → HSV
# -------------------------------------------------------------------
hsv = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2HSV
)
# -------------------------------------------------------------------
# 色ごとのHSV範囲を定義
#
# OpenCVのHSV:
#   H: 0～179
#   S: 0～255
#   V: 0～255
#
# 注意:
#   赤はH=0付近にあるため、本来は0付近と179付近の
#   2範囲で扱うことが多い。
#   今回のテスト画像では H=0 の赤だけなので1範囲でよい。
# -------------------------------------------------------------------

color_ranges = {
   "Red": {
      "lower": np.array([0, 100, 100]),
      "upper": np.array([10, 255, 255]),
      "draw_color": (0, 0, 255)
   },
   "Green": {
      "lower": np.array([50, 100, 100]),
      "upper": np.array([80, 255, 255]),
      "draw_color": (0, 255, 0)
   },
   "Blue": {
      "lower": np.array([100, 100, 100]),
      "upper": np.array([140, 255, 255]),
      "draw_color": (255, 0, 0)
   },
   "Yellow": {
      "lower": np.array([20, 100, 100]),
      "upper": np.array([40, 255, 255]),
      "draw_color": (0, 255, 255)
   },
}

#-------------------------------------------------------------------
# 検出結果用描画
#-------------------------------------------------------------------
result = image.copy()

#-------------------------------------------------------------------
# 色ごとに検出する
#-------------------------------------------------------------------
for color_name, params in color_ranges.items():
  lower = params["lower"]
  upper = params["upper"]
  draw_color = params["draw_color"]

  #-------------------------------------------------------------------
  # 指定職のマスクを作成
  #-------------------------------------------------------------------
  mask = cv2.inRange(hsv, lower, upper)

  #-------------------------------------------------------------------
  # マスクから輪郭を検出
  #-------------------------------------------------------------------
  contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  print(f"{color_name} :", len(contours))

  #-------------------------------------------------------------------
  # 輪郭ごとに処理
  #-------------------------------------------------------------------
  for i, contour in enumerate(contours):
    area = cv2.contourArea(contour) # 輪郭の面積を取得する
    if area < 500:
        continue

  x, y, w, h = cv2.boundingRect(contour)
  center_x = x + w // 2
  center_y = y + h // 2
    
  print(
      f"{color_name:6s} "
      f"輪郭[{i:4d}] "
      f"area={area:9.1f} "
      f"x={x:4d}, y={y:4d} "
      f"w={w:4d}, h={h:4d} "
      f"center=({center_x:4d}, {center_y:4d})"
  )

  # 外接長方形を描画
  cv2.rectangle(result, (x, y), (x+w, y+h), draw_color, 3)

  # 中心を描画
  cv2.circle(result, (center_x, center_y), 6, draw_color, -1)

  #-------------------------------------------------------------------
  # 色名を表示
  #-------------------------------------------------------------------
  cv2.putText(result, color_name, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, draw_color, 2)
#-------------------------------------------------------------------
# 画像表示
#-------------------------------------------------------------------
cv2.imshow("Original Image", image)
cv2.imshow("Multi Color Detection", result)

cv2.waitKey(0)
cv2.destroyAllWindows()