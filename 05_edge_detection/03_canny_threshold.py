"""
Cannyエッジ検出のしきい値を確認する : cv2.Canny()

背景との明るさ差が異なる3つの長方形を描画し、
Cannyのしきい値によって、どの境界が検出されるかを比較する。
"""

import cv2
import numpy as np


# 白い画像を作成
image = np.full((500, 800, 3), 255, dtype=np.uint8)

# 明るさの異なる長方形を描画
# 左: 黒
cv2.rectangle(
    image,
    (50 , 120),
    (220, 320),
    (0, 0, 0),
    -1
)
# 中央: 濃い灰色
cv2.rectangle(
    image,
    (315, 120),
    (485, 320),
    (180, 180, 180),
    -1
)
# 右: 薄い灰色
cv2.rectangle(
    image,
    (580, 120),
    (750, 320),
    (240, 240, 240),
    -1
)

# グレースケール変換
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Cannyエッジ検出
edges1 = cv2.Canny(gray, 30, 100)
edges2 = cv2.Canny(gray, 50, 150)
edges3 = cv2.Canny(gray, 100, 200)


# 表示
cv2.imshow("Original", image)
cv2.imshow("Gray", gray)
cv2.imshow("Canny 30-100", edges1)
cv2.imshow("Canny 50-150", edges2)
cv2.imshow("Canny 100-200", edges3)

cv2.waitKey(0)
cv2.destroyAllWindows()