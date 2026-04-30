import cv2
#drawing on the img

img1 = cv2.imread(r"C:\Users\Demet\OneDrive\Desktop\Peak Screenshots\IMG_8836.png") #loads picture
img2 = cv2.imread(r"C:\Users\Demet\OneDrive\Desktop\Peak Screenshots\IMG_8836.png")
shape = cv2.rectangle(img2,(50,50),(350,300),(255,0,0),2)
resize = cv2.resize(img1, (250, 250))
resize2 = cv2.resize(shape, (250, 250))
cv2.imshow(" normal dog picture", resize) #opens the picture in window
cv2.imshow('dog pig with shape', resize2)
cv2.waitKey(0)