#!/usr/bin/env python3
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

while True:
    ret, frame = cap.read()
    if not ret:
        print('cannot access webcam')
        break

    frame = cv2.resize(frame, (1000, 920))

    #media_pipe additions / hand tracking
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('title', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
