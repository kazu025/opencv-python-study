'''
二値画像から輪郭を検出する : cv2.findContours()

処理の流れ
  1. 画像を読み込む
  2. グレースケール画像へ変換する
  3. 二値化する
  4. 二値画像から輪郭を検出する
  5. 検出した輪郭を元画像に描画する
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

# 検出した輪郭を元画像に描画する
cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)

cv2.imshow("Original Image", image)
cv2.imshow("Gray Image", gray_image)
cv2.imshow("Binary Image", binary_image)
cv2.imshow("Contours", result_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

'''
JPEG画像
   ↓
imread()
   ↓
BGRカラー画像
   ↓
cvtColor()
   ↓
グレースケール
   ↓
threshold()
   ↓
二値画像
   ↓
findContours()
   ↓
輪郭データ
   ↓
drawContours()
   ↓
輪郭を画像上に表示
'''