import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"databaseURL":"https://cv-database-fc0e6-default-rtdb.firebaseio.com/"})

ref = db.reference('Students')

data= {

'2213438':{
    'last_attendance_time' : '2026-1-1  00:00:00',
    'name':'Anas Nahhas',
    'age':22,
    'gender':'male',
    'major':'AI',
    'year':2,
    'starting year':2021,
    'total_attendance':8,
    'status':'IN'
} ,
'2213433':{
'last_attendance_time' : '2026-1-1  00:00:00',
    'name':'Abd Zmailli',
    'age':30,
    'gender':'male',
    'major':'leader',
    'year':4,
    'starting year':2022,
    'total_attendance':5,
    'status':'IN'
}

}

for key, value in data.items():
    ref.child(key).set(value)