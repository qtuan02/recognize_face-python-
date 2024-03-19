import face_recognition
import os, sys
import cv2
import numpy as np


path = 'faces' #đường dẫn đến folder faces(là folder kho ảnh)
listFace = os.listdir(path) #danh sách tên các ảnh
listNameFaces = [] #danh sách chứa tên file ảnh(không có đuôi mở rộng)
listFaceEncodings = [] #chứa danh sách các ảnh mã hóa trong kho



#Bước 1: load từ kho, xác định và mã hóa
for item in listFace:
    face_image = face_recognition.load_image_file(f'{path}/{item}') #đọc ảnh thành dạng NumPy
    face_encoding = face_recognition.face_encodings(face_image)[0] #mã hóa ảnh

    listNameFaces.append(os.path.splitext(item)[0]) #lưu tên ảnh vào danh sách(chỉ tên, không có phần mở rộng)
    listFaceEncodings.append(face_encoding) #lưu ảnh đã mã hóa vào danh sách


#Hàm tính tỉ lệ giống nhau của các khuôn mặt trong camera và trong kho
def face_confidence(face_distance):
    value = 1.0 - face_distance
    return str(round(value * 100, 2)) + '%'


#Bước 2: khởi động camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    sys.exit("Khong tim thay nguon video")


while True:
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    #Bước 3: Tìm kiếm các khuôn mặt trong camera và mã hóa
    face_locations = face_recognition.face_locations(small_frame, 1, "cnn")
    face_encodings = face_recognition.face_encodings(small_frame, face_locations, 5, "small")

    face_names = []
    #Bước 4: Lấy từng khuôn mặt trong kho ảnh so sánh với từng khuôn mặt trong camera
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(listFaceEncodings, face_encoding, 0.5) #so sánh
        name = 'Unknown'
        confidence = 'Unknown'

        face_distances = face_recognition.face_distance(listFaceEncodings, face_encoding) #tính tỉ lệ giống nhau
        best_match_index = np.argmin(face_distances) #chọn vị trí ảnh có tỉ lệ giống cao nhất

        if matches[best_match_index]:
            name = listNameFaces[best_match_index]
            confidence = face_confidence(face_distances[best_match_index])

        face_names.append(f'{name}({confidence})')


    #Bước 5: Hiển thị kết quả lên camera
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, top - 30), (right, top), (0, 255, 0), -1)
        cv2.putText(frame, name.upper(), (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)

    cv2.imshow('Nhan dien khuon mat', frame)
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()