"""
輪郭を面積でフィルタする : cv2.contourArea()

Cannyでエッジを検出し、
findContours()で輪郭を取得する。

その後、輪郭面積が小さいものを除外し、
大きな物体だけを残す。
"""

import cv2
import numpy as np


# 白い画像を作成
image = np.full((500, 700, 3), 255, dtype=np.uint8)

# 黒い長方形
cv2.rectangle(
    image,
    (80 , 120),
    (280, 320),
    (0, 0, 0),
    -1
)
# 大きな円
cv2.circle(
    image,
    (500, 220),
    100,
    (0, 0, 0),
    -1
)

# 小さい図形
cv2.rectangle(
    image,
    (350, 80),
    (356, 95),
    (0, 0, 0),
    -1
)
cv2.circle(
    image,
    (380, 400),
    8,
    (0, 0, 0),
    -1
)
cv2.circle(
    image,
    (600, 400),
    5,
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
result_all = image.copy()
result_filter = image.copy()

# 検出した輪郭を描画
cv2.drawContours(
    result_all,
    contours,
    -1,
    (0,0,255),
    2
)
# 面積の閾値
MIN_AREA = 1000


# 輪郭情報を表示
print(f"検出した輪郭数:  {len(contours)}")
print(f"面積閾値:  {MIN_AREA}")
print()

for i, contour in enumerate(contours):
    area = cv2.contourArea(contour)

    x, y, w, h = cv2.boundingRect(contour)

    print(
        f"輪郭:[{i:2d}] "
        f"area={area:9.1f} "
        f"x={x:4d} y={y:4d} "
        f"w={w:4d} h={h:4d}"
    )

    # 小さい輪郭は無視
    if area < MIN_AREA:
        continue

    # 面積が大きい輪郭だけ描画
    cv2.drawContours(
        result_filter,
        [contour],
        -1,
        (0,0,255),
        2
    )

# 画像表示
cv2.imshow("Original", image)
cv2.imshow("Canny", edges)
cv2.imshow("All Contours", result_all)
cv2.imshow("Filtered Contours", result_filter)

cv2.waitKey(0)
cv2.destroyAllWindows()