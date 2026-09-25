'''
minAreaRect() で求めた回転長方形の向きを可視化する
  : cv2.minAreaRect()
  : cv2.boxPoints()
  : cv2.line()

処理の流れ
  1. 画像を読み込む
  2. グレースケール化する
  3. 二値化する
  4. 輪郭を検出する
  5. 小さな輪郭を面積で除外する
  6. minAreaRect() で最小外接長方形を求める
  7. 長方形の4頂点から長辺を求める
  8. 長辺の角度を atan2() で計算する
  9. 長方形の中心から、その向きに線を描画する

表示色
  緑 : minAreaRect() の回転長方形
  青 : 長方形の中心
  赤 : 長辺方向を示す線
'''

from pathlib import Path

import cv2
import numpy as np
import math

# 画像を読み込む
image = cv2.imread(str(Path(__file__).resolve().parents[1] / "images" / "private" / "sample03.jpg"))

if image is None:
    print("Error: Could not read the image. Check images/private (see README.md).")
    exit()

# グレースケール画像に変換
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#二値化
threshold_value = 128
ret, binary_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY_INV)

# 輪郭を検出する
contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 検出した輪郭数を表示する
print("輪郭数 :", len(contours))

# 戻画像をコピー
result_image = image.copy()

# この面積未満の輪郭は除外する
MIN_AREA = 500

# 各輪郭の面積を求める
for i, contour in enumerate(contours):
    # 輪郭の面積を求める
    area = cv2.contourArea(contour)
    #print(f"輪郭の面積[{i}] = {area}")

    if area < MIN_AREA:
        # 面積が一定以下の輪郭は除外する
        continue
    # -------------------------------------------------------------------
    # minAreaRect()
    # 回転を許した最小面積外接長方形
    # -------------------------------------------------------------------
    rect = cv2.minAreaRect(contour)
    # rectの内容
    (center_x, center_y), (rect_w, rect_h), angle = rect
    # -------------------------------------------------------------------
    # 長方形の4頂点を取得
    # -------------------------------------------------------------------
    box = cv2.boxPoints(rect)
    # 頂点0→1と頂点1→2の辺の長さを求める
    dx01 = box[1][0] - box[0][0]
    dy01 = box[1][1] - box[0][1]

    dx12 = box[2][0] - box[1][0]
    dy12 = box[2][1] - box[1][1]

    length01 = math.hypot(dx01, dy01)
    length12 = math.hypot(dx12, dy12)

    # -------------------------------------------------------------------
    # 長いほうの辺を選択
    # -------------------------------------------------------------------
    if length01 >= length12:
        dx = dx01
        dy = dy01
        long_length = length01
    else:
        dx = dx12
        dy = dy12
        long_length = length12

    # -------------------------------------------------------------------
    # 長辺の向きを角度へ変換
    # atan2()の結果はラジアンなので、degree()で度へ変換
    # -------------------------------------------------------------------
    direction_angle = math.degrees(math.atan2(dy, dx))

    # -------------------------------------------------------------------
    # 向きを示す線の最終店を計算
    # -------------------------------------------------------------------
    line_length = 60
    rad = math.radians(direction_angle)
    end_x = int(center_x + line_length * math.cos(rad))
    end_y = int(center_y + line_length * math.sin(rad))

    #-------------------------------------------------------------------
    # コンソール表示
    #-------------------------------------------------------------------
    print(
        f"輪郭[{i:4d}] "
        f"(area={area:9.1f}) : "
        f", 中心座標 : ({center_x:7.1f}, {center_y:7.1f})"
        f", サイズ : ({rect_w:7.1f}, {rect_h:7.1f})"
        f", raw_angle: ({angle:7.1f})"
        f", dirction: ({direction_angle:7.1f})"
    )
    #-------------------------------------------------------------------
    # 回転長方形を緑で描画
    #-------------------------------------------------------------------
    box_int = np.intp(box)
    cv2.drawContours(result_image, [box_int], 0, (0, 255,0), 2)

    #-------------------------------------------------------------------
    # 長方形の中心を青で描画
    #-------------------------------------------------------------------
    center = (int(center_x), int(center_y))
    cv2.circle(result_image, center, 5, (255, 0, 0), -1)

    #-------------------------------------------------------------------
    # 長辺方向を赤戦で描画
    #-------------------------------------------------------------------
    cv2.line(result_image, center, (end_x, end_y), (0,0,255), 3)
   

cv2.imshow("Original Image", image)
cv2.imshow("Binary Image", binary_image)
cv2.imshow("Direction", result_image)

cv2.waitKey(0)
cv2.destroyAllWindows()