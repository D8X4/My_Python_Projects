import cv2
#img loading normally

img = cv2.imread(r"C:\Users\Demet\OneDrive\Desktop\Peak Screenshots\IMG_8836.png")
if img is None:
    print('cannot open the image')
else:
    cv2.imshow("dog picture", img)
    cv2.waitKey(0)