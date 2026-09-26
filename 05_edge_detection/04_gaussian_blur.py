"""
GaussianBlurでノイズを減らしてからCannyエッジ検出する

元画像に細かなノイズを加え、
そのままCannyした場合と、
GaussianBlur後にCannyした場合を比較する。
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

# ノイズを抑える
noise = np.random.normal( # grayと同じサイズのランダムノイズ画像を作る
    0,
    25,
    gray.shape
)
noisy = gray.astype(np.float32) + noise
# 0~255に収める
noisy = np.clip(noisy, 0, 255)
# uint8型に戻す
noisy = noisy.astype(np.uint8)
# GoussianNlurをかける
blur = cv2.GaussianBlur(noisy, (5, 5), 0)

#ノイズあり画像をそのままCanny
edges_noisy =cv2.Canny(
    noisy,
    50,
    150
)

# GaussianBlur後にCanny
edges_blur = cv2.Canny(
    blur, 50, 150
)

# 表示
cv2.imshow("Original", gray)
cv2.imshow("Noisy", noisy)
cv2.imshow("Gaussian Blur", blur)
cv2.imshow("Canny Noisy", edges_noisy)
cv2.imshow("Canny Blur", edges_blur)

cv2.waitKey(0)
cv2.destroyAllWindows()