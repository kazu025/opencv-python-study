'''
輪郭の重心を求め、外接長方形の中心と比較する
  : cv2.moments()
  : cv2.boundingRect()
  : cv2.circle()

処理の流れ
  1. 画像を読み込む
  2. グレースケール化する
  3. 二値化する
  4. 輪郭を検出する
  5. 小さな輪郭を面積で除外する
  6. boundingRect() で外接長方形を求める
  7. 外接長方形の中心を求める
  8. moments() で輪郭の重心を求める
  9. 外接長方形の中心と輪郭重心を画像上に描画する

表示色
  赤 : 外接長方形
  青 : 外接長方形の中心
  緑 : 輪郭そのものの重心
'''

from pathlib import Path

import cv2

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
    # 輪郭を囲む長方形の x, y, w, h を取得する
    # -------------------------------------------------------------------
    x, y, w, h = cv2.boundingRect(contour)
    # 長方形の中心座標を計算する
    center_x = x + w // 2
    center_y = y + h // 2

    # -------------------------------------------------------------------
    # 輪郭のモーメントを計算
    # M["m00"]: 面積に相当する値
    # M["m10"]: x方向の位置を考慮した値
    # M["m01"]: y方向の位置を考慮した値
    # -------------------------------------------------------------------
    M = cv2.moments(contour)
    # m00 が 0 の場合は、重心を計算できないので除外する
    if M["m00"] == 0:
        continue
    # 輪郭の重心を計算する
    centroid_x = int(M["m10"] / M["m00"])
    centroid_y = int(M["m01"] / M["m00"])

    #-------------------------------------------------------------------
    # 輪郭の重心と外接長方形の中心を表示する
    #-------------------------------------------------------------------
    print(
        f"輪郭[{i:4d}] "
        f"(area={area:9.1f}) の長方形座標: "
        f"x={x:4d}, y={y:4d}, w={w:4d}, h={h:4d}"
        f", 中心座標: ({center_x:4d}, {center_y:4d})"
        f", 重心座標: ({centroid_x:4d}, {centroid_y:4d})"
    )
    #-------------------------------------------------------------------
    # 外接長方形を赤で描画する
    #-------------------------------------------------------------------
    cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #-------------------------------------------------------------------
    # 外接長方形の中心を青で描画する
    #-------------------------------------------------------------------
    cv2.circle(result_image, (center_x, center_y), 6, (255, 0, 0), -1)
    #-------------------------------------------------------------------
    # 輪郭の重心座標を緑で描画する
    #-------------------------------------------------------------------
    cv2.circle(result_image, (centroid_x, centroid_y), 6, (0, 255, 0), -1)

cv2.imshow("Original Image", image)
cv2.imshow("Binary Image", binary_image)
cv2.imshow("Result Image", result_image)

cv2.waitKey(0)
cv2.destroyAllWindows()