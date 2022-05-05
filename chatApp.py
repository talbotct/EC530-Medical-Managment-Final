from email import message
from flask import Flask, render_template, request, redirect, url_for
import os
import time
import json
from google.cloud import firestore

#Working towards web application for chat functionality
#TODO formating application screens

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ttaylor-med-api-3285443a6f89.json'

app = Flask(__name__, template_folder = "Template")
app.secret_key = "any random string"
app.config['SECRET_KEY'] = 'secret'

db = firestore.Client()
test1={
    u'email': u'user3@gmail.com',
    u'password': u'user3',
    u'uid': u'user3'
}
userRef = db.collection(u'userAccount')

currUser = None
userList = []
chatID = None

userData = {}


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    return render_template("signup.html")

@app.route("/signupCheck", methods = ["GET", "POST"])
def signupCheck():
    global userData
    if(request.method == "POST"):
        req = dict(request.form)
        flag = 0
        # TODO, implement database query to check if user already exists.
        # Will do for app implementation
        # print(req)
        # query = userRef.where(u"uid", u"==", True).stream()
        # print(query)

        # for doc in query:
        #     print(f'{doc.id} => {doc.to_dict()}')

        # for i in query:
        #     print(i)
        #     if(i["uid"] == req["uid"]):
        #         flag = 1
        #         break
        regDict = {
            "email": req["email"],
            "uid": req["uid"],
            "password": req["password"]
        }

        if flag == 0:
            #holder = userRef.add(regDict)
            uid = req["uid"]
            userData[uid] = {}
            userData[uid]["chatID"] = None
            userData[uid]["userList"] = []
            userData[uid]["msgList"] = {}
            return render_template("dashboard.html", uid = req["uid"])
        else:
            return render_template("error.html", message = "User already exists")
            
        
    
    return render_template("signup.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/loginCheck", methods = ["GET", "POST"])
def loginCheck():
    global userData
    if(request.method == "POST"):
        req = dict(request.form)
        flag = 0

        # TODO, implement database query to check if user password is correct
        # Will do for app implementation
        # print(req)
        # query = userRef.where(u"uid", u"==", True).stream()
        # print(query)

        # for doc in query:
        #     print(f'{doc.id} => {doc.to_dict()}')

        # for i in query:
        #     print(i)
        #     if(i["uid"] == req["uid"]):
        #         flag = 1
        #         break

        regDict = {
            "email": req["email"],
            "uid": req["uid"],
            "password": req["password"]
        }

        if flag == 1:
            #holder = userRef.add(regDict)
            uid = req["uid"]
            userData[uid] = {}
            userData[uid]["chatID"] = None
            userData[uid]["userList"] = []
            userData[uid]["msgList"] = {}
            return render_template("dashboard.html", uid = req["uid"])
        else:
            return render_template("error.html", message = "Incorrect Password")        

@app.route("/dashboard", methods = ["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/connectUser", methods = ["GET", "POST"])
def connectUser():
    global userList
    #file = open(userFile.txt, "r")
    #userList = file.readlines()
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug = True, threaded = True)
