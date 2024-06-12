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
email = "kingcanut@gmail.com"
password = "00190029"
user = auth.sign_in_with_email_and_password(email, password)
id_token = user['idToken']
db = firebase.database()

