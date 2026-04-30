#!/usr/bin/env python3
import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()
frame = None
canvas = None
prev_x = None
prev_y = None

while True:
    ret, frame = cap.read()
    if not ret:
        print('cannot access webcam')
        break

    frame = cv2.resize(frame, (1000, 920))
    if canvas is None:
        canvas = np.zeros_like(frame)

    # media_pipe additions / hand tracking
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            # index finger detection
            if hand.landmark[8].y < hand.landmark[6].y:
                x = hand.landmark[8].x * 1000
                y = hand.landmark[8].y * 920
                newx = int(x)
                newy = int(y)

                # debug statements
                # print(newx, newy)
                # print(x, y)
                # print('index finger debug')
                if prev_x is not None:
                    cv2.line(canvas, (prev_x, prev_y), (newx, newy), (0, 255, 0), 2)
                prev_x = newx
                prev_y = newy
            else:
                prev_x = None
                prev_y = None

    frame = cv2.addWeighted(frame, 1, canvas, 0.5, 0)
    cv2.imshow('title', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('c'):
        canvas = np.zeros_like(frame)

cap.release()
cv2.destroyAllWindows()
