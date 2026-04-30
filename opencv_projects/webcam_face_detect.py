import cv2
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)# 0 = default webcam
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (1000, 920))
prev = time.time()
faces = []
frame_count = 0


while True:
    ret, frame = cap.read()
    fps = 1 / (time.time() - prev)
    prev = time.time()
    frame_count += 1

    if not ret:
        print('cannot access webcam')
        break

    frame = cv2.resize(frame, (1000, 920))

    if frame_count % 5 == 0:
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=5)

    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    for (x, y, w, h) in faces:
        cv2.putText(frame, "human detected", (x-5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)

    out.write(frame)
    cv2.imshow("faces detected:", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()