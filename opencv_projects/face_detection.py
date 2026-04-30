import cv2

img = cv2.imread(r"C:\Users\Demet\OneDrive\Desktop\Peak Screenshots\group_pic.jpg")

if img is None:
    print('cannot open the image')

else:
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=5)
    print(f"faces found: {len(faces)}")

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow(f"faces detected: {len(faces)}", img)
    cv2.waitKey(0)