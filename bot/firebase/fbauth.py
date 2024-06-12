import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyBUAKY_gfQGaT2JIlRCIQnmnjWCFcdz15s",
    'authDomain': "telegrambot-7a928.firebaseapp.com",
    'projectId': "telegrambot-7a928",
    'storageBucket': "telegrambot-7a928.appspot.com",
    'messagingSenderId': "893954792155",
    'appId': "1:893954792155:web:406477807c0f2204058afe",
    'measurementId': "G-PZSM6KEE3S",
    'databaseURL': "https://telegrambot-7a928-default-rtdb.asia-southeast1.firebasedatabase.app/project"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

db = firebase.database()

data = {
    "subject_name": "Nanananna",
    "subject_code": "222222"
}
# db.child("Subject List").child("222222").update({"subject_name" : "AYer"})

# dba = { "Subject List/222222" : {"subject_name": "Proper Name", "subject_code" : 123432}, "Subject List/352822": {"subject_name" : "another proper name ", "subject_code" : 352822}}

# db.update(dba)

sub = db.child("Subject List").get()

check_tutor = db.child("users").child(373468118).child("tutor").get()



# for s in sub.each():
#     print(s.val())