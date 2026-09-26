"""
Cannyエッジ画像から輪郭を検出する : cv2.findContours()

GaussianBlurでノイズを減らし、
Cannyでエッジ画像を作成し、
findContours()で輪郭を取得する。
"""

import cv2
import numpy as np


# 白い画像を作成
image = np.full((500, 700, 3), 255, dtype=np.uint8)

# 黒い長方形
cv2.rectangle(
    image,
    (100 , 120),
    (300, 320),
    (0, 0, 0),
    -1
)
# 黒い円
cv2.circle(
    image,
    (500, 220),
    100,
    (0, 0, 0),
    -1
)

# グレースケール変換
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# GaussianBlur
# 画像を少しぼかしてノイズを減らす処理　5x5の範囲
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny エッジ検出
edges = cv2.Canny(blur, 50, 150)

# 輪郭検出
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 輪郭描画用に元画像をコピー
result = image.copy()

# 検出した輪郭を描画
cv2.drawContours(
    result,
    contours,
    -1,
    (0,0,255),
    2
)

# 輪郭情報を表示
print(f"検出した輪郭数:  {len(contours)}")

for i, contour in enumerate(contours):
    area = cv2.contourArea(contour)

    x, y, w, h = cv2.boundingRect(contour)

    print(
        f"輪郭:[{i:2d}] "
        f"area={area:9.1f} "
        f"x={x:4d} y={y:4d} "
        f"w={w:4d} h={h:4d}"
    )

# 画像表示
cv2.imshow("Original", image)
cv2.imshow("Gray", gray)
cv2.imshow("Blur", blur)
cv2.imshow("Canny", edges)
cv2.imshow("Contours", result)

cv2.waitKey(0)
cv2.destroyAllWindows()