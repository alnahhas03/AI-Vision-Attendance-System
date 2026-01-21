import cv2
import os
import pickle
import face_recognition
import firebase_admin
from firebase_admin import credentials, db, storage
from firebase_admin.storage import bucket


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL":"https://cv-database-fc0e6-default-rtdb.firebaseio.com/",
    "storageBucket":"cv-database-fc0e6.firebasestorage.app"
})


img_file = "Images"
img_file_list = os.listdir(img_file)

imgList = []
IDs = []
for path in img_file_list:
    imgList.append(cv2.imread(os.path.join(img_file,path)))
    IDs.append(os.path.splitext(path)[0])

    filename = f'{img_file}/{path}'
    bucket = storage.bucket()
    blob= bucket.blob(filename)
    blob.upload_from_filename(filename)

def findEncodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist


encoddelist = findEncodings(imgList)
final_encode = [encoddelist, IDs]
print(encoddelist)

#print("open------------------------")
file = open("encodefile.p", "wb")
pickle.dump(final_encode, file)
file.close()

#print("cloced--------------------")