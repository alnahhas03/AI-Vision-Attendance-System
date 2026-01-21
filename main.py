import os
import pickle
import face_recognition
import cv2
import cvzone
import numpy as np
import firebase_admin
from firebase_admin import credentials, db, storage
from firebase_admin.storage import bucket
from datetime import datetime


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL":"https://cv-database-fc0e6-default-rtdb.firebaseio.com/",
    "storageBucket":"cv-database-fc0e6.firebasestorage.app"
})

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

#print("open ----------------------")
file = open("encodefile.p", "rb")
final_encode = pickle.load(file)
encoddelist, IDs = final_encode
file.close()
#print("cloced ----------------------")

imageback = cv2.imread('Resources/Background.png')

FolderModePath = 'Resources/Modes'
modePathLest = os.listdir(FolderModePath)
imgModelist = []
for path in modePathLest:
    imgModelist.append(cv2.imread(os.path.join(FolderModePath, path)))

mainType = 0
counter = 0
id = -1
imgStudent = []
bucket = storage.bucket()
while(True):
    sucess, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    encodeLocation = face_recognition.face_locations(imgS)
    encodeCurrFace = face_recognition.face_encodings(imgS)
    encodeCurrFace = np.array(encodeCurrFace)
    
    imageback[162:162+480, 55:55 + 640] = img
    imageback[44:44 + 633, 808:808 + 414] = imgModelist[mainType]

    if encodeLocation:
        for faceLoc, faceInc in zip(encodeLocation, encodeCurrFace):
            matches = face_recognition.compare_faces(encoddelist, faceInc)
            faceDis = face_recognition.face_distance(encoddelist, faceInc)
            #print("matches", matches)
            #print("faceDis", faceDis)

            machindx = np.argmin(faceDis)
            print("machindx", machindx)

            if matches[machindx]:
                #print("the image is detected")
                #print(IDs[machindx])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = x1 + 55, y1 + 162, x2 - x1, y2 - y1
                imageback = cvzone.cornerRect(imageback, bbox, rt=0)
                id = IDs[machindx]
                if counter == 0:
                    cvzone.putTextRect(imageback, "Loading", (200,300))
                    cv2.imshow('face attendance', imageback)
                    cv2.waitKey(1)
                    counter= 1
                    mainType = 1

        if counter!= 0:
            if counter ==1:
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                blob = bucket.get_blob(f'Images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), dtype=np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2RGB)
                objectdatetime = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondElaps = (datetime.now() - objectdatetime).total_seconds()
                print(secondElaps)

                if secondElaps >50:
                    ref = db.reference(f'Students/{id}')
                    update_att = studentInfo['total_attendance']
                    update_att+=1
                    ref.child('total_attendance').set(update_att)
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    counter = 0
                    mainType = 3
                    imageback[44:44 + 633, 808:808 + 414] = imgModelist[mainType]

            if 10<counter<20:
                mainType = 2

            imageback[44:44 + 633, 808:808 + 414] = imgModelist[mainType]

            if mainType != 3:

                if counter<=10:
                    cv2.putText(imageback, str(update_att), (861,125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

                    cv2.putText(imageback, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    cv2.putText(imageback, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    cv2.putText(imageback, str(studentInfo['status']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 2)

                    cv2.putText(imageback, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 2)

                    cv2.putText(imageback, str(studentInfo['starting year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 2)

                    (w,h),_ =  cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 2)
                    offset = (414-w)//2

                    cv2.putText(imageback, str(studentInfo['name']), (808+offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 2)

                    imgStudent = cv2.resize(imgStudent, (216, 216))
                    imageback[175:175+216, 909:909+216] = imgStudent

            counter+=1

            if counter>=20:
                counter = 0
                mainType = 0
                studentInfo = []
                imgStudent = []
                imageback[44:44 + 633, 808:808 + 414] = imgModelist[mainType]
    else:
        mainType=0
        counter=0
    cv2.imshow('face attendance', imageback)
    cv2.waitKey(1)