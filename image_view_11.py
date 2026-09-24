'''
輪郭を多角形近似して、図形の種類を判定する
  : cv2.arcLength()
  : cv2.approxPolyDP()
  : cv2.minAreaRect()

処理の流れ
  1. 画像を読み込む
  2. グレースケール化する
  3. 白黒を反転して二値化する
  4. 輪郭を検出する
  5. 輪郭の周囲長を求める
  6. approxPolyDP() で輪郭を多角形に近似する
  7. 近似された頂点数から図形を判定する
  8. 円と楕円は縦横比なども使って判定する
  9. 判定結果を画像上に表示する

判定の基本
  頂点数 3     : Triangle
  頂点数 4     : Rectangle / Square
  頂点数 5以上 : Circle / Ellipse候補
'''

import cv2
import math

# -------------------------------------------------------------------
# 画像を読み込む
# -------------------------------------------------------------------
image = cv2.imread("images/sample03.jpg")

if image is None:
    print("Error: Could not read the image.")
    exit()

# -------------------------------------------------------------------
# グレースケール画像に変換
# -------------------------------------------------------------------
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# -------------------------------------------------------------------
# 二値化
# 白背景、黒図形　なので、THRESH_BINARY_INVとする
# -------------------------------------------------------------------
threshold_value = 128
ret, binary_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY_INV)

# -------------------------------------------------------------------
# 輪郭を検出する
# -------------------------------------------------------------------
contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 検出した輪郭数を表示する
print("輪郭数 :", len(contours))

# 戻画像をコピー
result_image = image.copy()

# -------------------------------------------------------------------
# 輪郭処理
# -------------------------------------------------------------------
# この面積未満の輪郭は除外する
MIN_AREA = 500

# 各輪郭の面積を求める
for i, contour in enumerate(contours):
    # 輪郭の面積を求める
    area = cv2.contourArea(contour)

    if area < MIN_AREA:
        # 面積が一定以下の輪郭は除外する
        continue
    # -------------------------------------------------------------------
    # 輪郭の周囲長
    # -------------------------------------------------------------------
    perimeter = cv2.arcLength(contour, True)
    # -------------------------------------------------------------------
    # 輪郭を多角形に近似
    # epsilon: 元の輪郭からどこまで離れてよいか 今回は周囲長の2%
    # -------------------------------------------------------------------
    epsilon = 0.02 * perimeter  # 
    approx = cv2.approxPolyDP(contour, epsilon, True)   # 特徴を維持したまま少ない頂点へ単純化
    #近似後の頂点数
    vertices = len(approx)
    # -------------------------------------------------------------------
    # minAreaRect()の縦横比を調べる
    # -------------------------------------------------------------------
    rect = cv2.minAreaRect(contour)
    # rectの内容
    (center_x, center_y), (w, h), angle = rect

    if w > 0 and h > 0:
        aspect_ratio = max(w, h) / min(w, h)
    else:
        aspect_ratio = 0

    # -------------------------------------------------------------------
    # 円形度
    # 真円につかづく→1.0
    # -------------------------------------------------------------------
    circularity = (4.0 * math.pi * area / (perimeter * perimeter))

    # -------------------------------------------------------------------
    # 図形判定 頂点数と、アスペクト比、円形度で図形を判定する
    # -------------------------------------------------------------------
    if vertices == 3:
        shape_name = "Triangle"
    elif vertices ==4:
        # 正方形と長方形を縦横比で区別
        if aspect_ratio < 1.10:
            shape_name = "Square"
        else:
            shape_name = "Rectangle"
    else:
        # 円と楕円を判定
        if (aspect_ratio < 1.10 and circularity > 0.08):
            shape_name = "Circle"
        else:
            shape_name = "Ellipse"
    
    #-------------------------------------------------------------------
    # コンソール表示
    #-------------------------------------------------------------------
    print(
        f"輪郭[{i:4d}] "
        f"(area={area:9.1f}) : "
        f", vertex : ({vertices:2d})"
        f", ratio  : ({aspect_ratio:5.2f})"
        f", circulatiry: ({circularity:5.1f})"
        f", {shape_name})"
    )
    #-------------------------------------------------------------------
    # 近似した輪郭を緑で表示
    #-------------------------------------------------------------------
    cv2.drawContours(result_image, [approx], -1, (0,255,0), 3)

    #-------------------------------------------------------------------
    # 図形名を表示
    #-------------------------------------------------------------------
    x, y, bw, by = cv2.boundingRect(contour)
    cv2.putText(result_image, shape_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

#-------------------------------------------------------------------
# 画像表示
#-------------------------------------------------------------------
cv2.imshow("Original Image", image)
cv2.imshow("Binary Image", binary_image)
cv2.imshow("Direction", result_image)

cv2.waitKey(0)
cv2.destroyAllWindows()