import cv2
import os
#img loading normally
path = r"C:\Users\Demet\OneDrive\Desktop\Peak Screenshots\IMG_9071.jpeg"
img = cv2.imread(path)

if img is None:
    print(f"cannot open image {path}")
else:

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=5)
    cv2.imshow('faces detected', grey)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    filename = os.path.basename(path)
    print(f"image {filename}")
    print(f'dimensions: {img.shape[:2]}')
    print(f"faces found: {len(faces)}")
    print(f"saved to greyscale")
    cv2.imwrite("greyscale.jpg", grey) #saves greyscale picture
    print("saved faces detected")
    cv2.imwrite("faces_Detected.jpg", img) #makes files with picture of faces in boxes

