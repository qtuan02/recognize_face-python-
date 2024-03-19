import time
import tkinter as tk
from tkinter import simpledialog
import face_recognition
import os, sys
import cv2


path = "faces/"
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    sys.exit("Khong tim thay nguon video")

start_time = None
while True:
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(small_frame)

    if len(face_locations) == 1:
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left - 21, top - 101), (right + 26, bottom + 36), (0, 255, 0), 1)
            cv2.putText(frame, "DANG LUU", (left + 26, top - 100), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 2)
            if start_time is None:
                start_time = time.time()

            elif time.time() - start_time >= 3:
                face_image = frame[top - 120:bottom + 30, left - 20:right + 25]

                root = tk.Tk()
                root.withdraw()
                name = simpledialog.askstring("Nhap ten anh", "Ten:")

                if name is None:
                    sys.exit()
                if name:
                    image_name = f"{name}.jpg"
                    cv2.imwrite(os.path.join(path, image_name), face_image)
                    sys.exit()

    cv2.imshow('Dang ky', frame)
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()