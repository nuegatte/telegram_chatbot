import pyrebase
import os


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
"""
push - auto-gen key
set - manually set key
"""
def dbpush():
    while True:
        print("Please choose an option:")
        print("1. To do list")
        print("2. studnetinfo")
        print("q. Quit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            activity = input("Activity name : ") 
            purpose = input("Why? : ")
            deadline = input("Due Day : ")
            dt = {"Activity": activity, "purpose" : purpose, "Deadline" : deadline}
            db.child("Todolist").child(activity).set(dt)
            # Add functionality for Option 1 here
        elif choice == '2':
            student_id = input("Student ID: ")
            student_name = input("Student Name: ")
            course_name = input("Course Name: ")
            dt = {"ID": student_id, "Name": student_name, "Course": course_name}
            db.child("studentList").child(f"{student_name}'s info").set(dt)
            # Add functionality for Option 2 here
        elif choice.lower() == 'q':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or q to quit.")

dbpush()
# dt = {"name": "Alkin", "age" :12, "address" : ["new york", "new street" ]}
# db.child("branch").child("employee").child("male employee").child("alkin's info").push(dt)
# #  
# dt = { "age" :12, "address" : ["new york", "new street" ]}
# db.child("Alkin").set(dt) # set primary key as Alkin

# storage options
storage = firebase.storage()

# upload to storage
def upload():
    file = input("File name you want to upload to storage: ")
    cloudfilename = input("File name in storage: ")

    # Check if the file exists
    if os.path.isfile(file):
        storage.child(cloudfilename).put(file)
        print(f"File '{file}' successfully uploaded to '{cloudfilename}'")
    else:
        print(f"Error: File '{file}' not found.")


# login options 

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

def menu():
    ans = input("new user? y/n")
    if ans== 'y':
        signup()
    elif ans == 'n':
        login()