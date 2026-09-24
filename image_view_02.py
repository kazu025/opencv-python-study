'''
sample.jpg
    ↓
cv2.imread()
    ↓
カラー画像
(H, W, 3)
BGR
    ↓
cv2.cvtColor()
    ↓
グレースケール
(H, W)
0～255
    ↓
cv2.threshold()
    ↓
二値画像
(H, W)
0 または 255
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


print("Color shape: ", image.shape)
print("Gray shape: ", gray_image.shape)
print("Binary shape: ", binary_image.shape)


print("threshold = ", ret)

print("Gray pixel :", gray_image[100, 200])
print("Binary pixel :", binary_image[100, 200])

cv2.imshow("Color Image", image)
cv2.imshow("Gray Image", gray_image)
cv2.imshow("Binary Image", binary_image)

cv2.waitKey(0)
cv2.destroyAllWindows()