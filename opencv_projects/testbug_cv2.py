import cv2
trackers = [x for x in dir(cv2) if 'Tracker' in x]
print(trackers)