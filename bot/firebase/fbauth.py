import pyrebase
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import logging

firebaseConfig = {
    'apiKey': "AIzaSyBUAKY_gfQGaT2JIlRCIQnmnjWCFcdz15s",
    'authDomain': "telegrambot-7a928.firebaseapp.com",
    'projectId': "telegrambot-7a928",
    'storageBucket': "telegrambot-7a928.appspot.com",
    'messagingSenderId': "893954792155",
    'appId': "1:893954792155:web:406477807c0f2204058afe",
    'measurementId': "G-PZSM6KEE3S",
    'databaseURL': "https://telegrambot-7a928.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)
# auth = firebase.auth()

# storage options
storage = firebase.storage()

# upload to storage
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