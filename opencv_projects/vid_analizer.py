import cv2

cap = cv2.VideoCapture(r"C:\Users\Demet\Downloads\gettyimages-1202137546-640_adpp.mp4")  # file instead of camera index
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))
frame_count = 0
saved = 0
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.05, minNeighbors=3, minSize=(20,20))
    frame_count += 1

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,255), 2)
        cv2.putText(frame, "spotted", (x-5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    out.write(frame)
    print(f"frame {frame_count}/{total_frames}", end="\r")


print('finished')
out.release()
cap.release()