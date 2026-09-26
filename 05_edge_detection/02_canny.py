"""
Cannyエッジ検出を試す : cv2.Canny()
(明るさの変化量を見ている)

cv2.Canny()の閾値を変える。

白地に黒い図形を描画し、
図形の境界部分をエッジとして検出する。
"""

import cv2
import numpy as np


# 白い画像を作成
image = np.full((500, 700, 3), 255, dtype=np.uint8)

# 黒い長方形
cv2.rectangle(
    image,
    (100, 100),
    (300, 300),
    (0, 0, 0),
    -1
)

# 黒い円
cv2.circle(
    image,
    (500, 200),
    100,
    (0, 0, 0),
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