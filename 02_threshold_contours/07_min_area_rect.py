'''
輪郭を、回転を許した最小面積の長方形で囲む
  : cv2.minAreaRect()
  : cv2.boxPoints()

処理の流れ
  1. 画像を読み込む
  2. グレースケール化する
  3. 二値化する
  4. 輪郭を検出する
  5. 小さな輪郭を面積で除外する
  6. boundingRect() で水平・垂直な外接長方形を求める
  7. minAreaRect() で回転を許した最小面積長方形を求める
  8. 2種類の長方形を画像に描画して比較する

表示色
  赤 : boundingRect() の長方形
  緑 : minAreaRect() の長方形
'''

from pathlib import Path

import cv2
import numpy as np

image = cv2.imread(str(Path(__file__).resolve().parents[1] / "images" / "private" / "sample02.jpg"))

if image is None:
    print("Error: Could not read the image. Check images/private (see README.md).")
    exit()
# グレースケール画像に変換
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#二値化
threshold_value = 128
ret, binary_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)

# 輪郭を検出する
# cv2.findContours() は、白い部分の輪郭を検出するので、二値化の際に白い部分が対象物になるようにする必要がある   
# contoursには、見つかった輪郭の座標が格納される
# RETR_EXTERNAL : 外側の輪郭のみを検出する
# CHAIN_APPROX_SIMPLE : 輪郭の点の座標を圧縮して格納する
# 黒が背景で白が対象物になるように二値化する必要がある
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
    # boundingRect()
    # 水平・垂直な外接長方形
    # -------------------------------------------------------------------
    x, y, w, h = cv2.boundingRect(contour)
    # 外接長方形を赤で描画する
    cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # -------------------------------------------------------------------
    # minAreaRect()
    # 回転を許した最小面積外接長方形
    # -------------------------------------------------------------------
    rect = cv2.minAreaRect(contour)
    # rectの内容
    (center_x, center_y), (rect_w, rect_h), angle = rect
    # 長方形の4頂点を取得
    box = cv2.boxPoints(rect)
    # 描画用に整数に変換
    box = np.intp(box)
    # 回転長方形を描画
    cv2.drawContours(result_image, [box], 0, (0,255,0), 2)

    #-------------------------------------------------------------------
    # コンソール表示
    #-------------------------------------------------------------------
    print(
        f"輪郭[{i:4d}] "
        f"(area={area:9.1f}) の長方形座標: "
        f", 中心座標: ({center_x:7.1f}, {center_y:7.1f})"
        f", サイズ　: ({rect_w:7.1f}, {rect_h:7.1f})"
        f", Angle  : ({angle:7.1f})"
    )

cv2.imshow("Original Image", image)
cv2.imshow("Binary Image", binary_image)
cv2.imshow("Result Image", result_image)

cv2.waitKey(0)
cv2.destroyAllWindows()