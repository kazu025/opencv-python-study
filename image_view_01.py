import cv2

image = cv2.imread("images/sample01.jpg")

if image is None:
    print("Error: Could not read the image.")
    exit()

print("カラー画像")
print("type : ", type(image))
print("shape: ", image.shape)

#100行目 200列目の画素を見る
pixel = image[100, 200]
print("pixel value: ", pixel)

# グレースケール画像に変換
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print("グレースケール画像")
print("type : ", type(gray_image))
print("shape: ", gray_image.shape)

print("グレースケール")
print("shape : ", gray_image.shape)
print("pixel value : ", gray_image[100, 200])

cv2.imshow("Color Image", image)
cv2.imshow("Gray Image", gray_image)

cv2.waitKey(0)
cv2.destroyAllWindows()