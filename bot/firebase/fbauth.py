import pyrebase



firebaseConfig = {
    'apiKey': "AIzaSyBUAKY_gfQGaT2JIlRCIQnmnjWCFcdz15s",
    'authDomain': "telegrambot-7a928.firebaseapp.com",
    'projectId': "telegrambot-7a928",
    'storageBucket': "telegrambot-7a928.appspot.com",
    'messagingSenderId': "893954792155",
    'appId': "1:893954792155:web:406477807c0f2204058afe",
    'measurementId' : "G-PZSM6KEE3S",
    'databaseURL': "https://telegrambot-7a928.firebaseio.com"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def signup():
    email = input("enter yur email: ")
    password = input("password: ")

    try :
        user = auth.create_user_with_email_and_password(email,password)
        print("sucessaccount")

    except:
        print("email exists dumbdumb")


def login():
    email = input("enter yur email: ")
    password = input("password: ")
    try :
        user = auth.sign_in_with_email_and_password(email,password)
        print("logging in...")

    except:
        print("pass/email error, input again  ")



ans = input("new user? y/n")
if ans== 'y':
    signup()
elif ans == 'n':
    login()