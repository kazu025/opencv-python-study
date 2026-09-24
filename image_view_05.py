'''
輪郭を長方形で囲み、位置と大きさを取得する
  : cv2.boundingRect()

処理の流れ
  1. 画像を読み込む
  2. グレースケール画像へ変換する
  3. 二値化する
  4. 輪郭を検出する
  5. 小さな輪郭を面積で除外する
  6. 輪郭を囲む長方形の x, y, w, h を取得する
  7. 元画像に長方形を描画する
'''

import cv2

image = cv2.imread("images/sample02.jpg")

if image is None:
    print("Error: Could not read the image.")
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

    # 輪郭を囲む長方形の x, y, w, h を取得する
    x, y, w, h = cv2.boundingRect(contour)
    print(
        f"輪郭[{i:4d}] "
        f"(area={area:9.1f}) の長方形座標: "
        f"x={x:4d}, y={y:4d}, w={w:4d}, h={h:4d}"
    )
    # 元画像に長方形を描画する
    cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)


cv2.imshow("Original Image", image)
cv2.imshow("Binary Image", binary_image)
cv2.imshow("Result Image", result_image)

cv2.waitKey(0)
cv2.destroyAllWindows()