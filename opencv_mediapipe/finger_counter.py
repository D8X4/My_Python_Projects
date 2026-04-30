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

    # media_pipe additions / hand tracking
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    count = 0

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            count = 0
            # index finger detection
            if hand.landmark[8].y < hand.landmark[6].y:
                count += 1
                # print('index finger up')
            # thumb finger detection
            if hand.landmark[4].x < hand.landmark[3].x:
                count += 1
                # print('thumb finger up')
            # middle finger detection
            if hand.landmark[12].y < hand.landmark[10].y:
                count += 1
                # print('middle finger up')
            # ring finger detection
            if hand.landmark[16].y < hand.landmark[14].y:
                count += 1
                # print('ring finger up')
            # pinky finger detection
            if hand.landmark[20].y < hand.landmark[18].y:
                count += 1
                # print('pinky finger up')

    cv2.putText(frame, f"Finger Counter: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('title', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
