import cv2
#resizing the image

img = cv2.imread(r"C:\Users\Demet\OneDrive\Desktop\Peak Screenshots\IMG_8836.png") #loads picture
resized = cv2.resize(img, (250, 250)) #resizes the picture

if img is None:
    print('cannot open the image')
else:
    cv2.imshow("dog picture", resized) #opens the picture in window
    cv2.waitKey(0)