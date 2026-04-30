import cv2
import time

cap = cv2.VideoCapture(r"C:\Users\Demet\Downloads\mixkit-young-man-walking-listening-to-music-from-his-headphones-4855-hd-ready.mp4")

ret, frame = cap.read()
bbox = cv2.selectROI("select object", frame, False)
tracker = cv2.legacy.TrackerKCF_create()
tracker.init(frame, bbox)

prev = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fps = 1 / (time.time() - prev)
    prev = time.time()

    success, bbox = tracker.update(frame)

    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, "tracking", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    else:
        cv2.putText(frame, "lost", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()