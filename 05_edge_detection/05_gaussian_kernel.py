"""
GaussianBlurのカーネルサイズを比較する

同じノイズ画像に対して、
(3, 3)、(5, 5)、(11, 11) のGaussianBlurを適用し、
Cannyエッジ検出の結果を比較する。
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

# ノイズ生成
noise = np.random.normal( # grayと同じサイズのランダムノイズ画像を作る
    0,
    25,
    gray.shape
)
# もの画像にノイズを加える
noisy = gray.astype(np.float32) + noise
# 0~255に収める
noisy = np.clip(noisy, 0, 255)
# uint8型に戻す
noisy = noisy.astype(np.uint8)
# GoussianNlurをかける
blur3 = cv2.GaussianBlur(noisy, (3, 3), 0)
blur5 = cv2.GaussianBlur(noisy, (5, 5), 0)
blur11 = cv2.GaussianBlur(noisy, (11, 11), 0)

#ノイズあり画像をそのままCanny
edge3 =cv2.Canny(blur3, 50, 150)
edge5 =cv2.Canny(blur5, 50, 150)
edge11 =cv2.Canny(blur11, 50, 150)

# 表示
cv2.imshow("Noisy", noisy)

cv2.imshow("Blur 3x3", blur3)
cv2.imshow("Blur 5x5", blur5)
cv2.imshow("Blur 11x11", blur11)

cv2.imshow("Canny 3x3", edge3)
cv2.imshow("Canny 5x5", edge5)
cv2.imshow("Canny 11x11", edge11)

cv2.waitKey(0)
cv2.destroyAllWindows()