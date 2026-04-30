import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ret, frame = cap.read()
frame = cv2.resize(frame, (640, 480))
bbox = cv2.selectROI("select object", frame, False)
tracker = cv2.legacy.TrackerKCF_create()
tracker.init(frame, bbox)
prev = time.time()
frame_count = 0

small = cv2.resize(frame, (320, 240))
success, bbox_small = tracker.update(small)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1000, 920))
    fps = 1 / (time.time() - prev)
    prev = time.time()
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    success, bbox = tracker.update(frame)


    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, "tracking", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    else:
        cv2.putText(frame, "lost press R to reselect", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("tracker", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        bbox = cv2.selectROI("select object", frame, False)
        tracker = cv2.legacy.TrackerCSRT_create()
        tracker.init(frame, bbox)

cap.release()
cv2.destroyAllWindows()
print('finished ')