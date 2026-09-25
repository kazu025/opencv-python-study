from pathlib import Path

import cv2

image = cv2.imread(str(Path(__file__).resolve().parents[1] / "images" / "private" / "sample01.jpg"))
if image is None:
    print("Error: Could not read the image. Check images/private (see README.md).")
    exit()
# 画面サイズ表示
print("image shape:", image.shape)

# 画像を表示
cv2.imshow('Sample Image', image)

print(type(image))
print(image[0,0])
# キー入力待ち
cv2.waitKey(0)
cv2.destroyAllWindows()
