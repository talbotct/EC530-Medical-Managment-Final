from email import message
from flask import Flask, render_template, request, redirect, url_for, session
import os
import time
import json
from google.cloud import firestore
import requests
from requests.auth import HTTPDigestAuth

from users import *
from devices import *
from chats import *

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ttaylor-med-api-3285443a6f89.json'

app = Flask(__name__, template_folder = "templates")
api = Api(app)
app.secret_key = "secret"
app.config['SECRET_KEY'] = 'secret'

db = firestore.Client()

userRef = db.collection(u'users')

currUser = None
userList = []
chatID = None
userID = "tal"

api.add_resource(user, '/user/<string:username>')
api.add_resource(deviceList, '/device/')
api.add_resource(device, '/device/<string:deviceID>')
api.add_resource(chatList, '/chat/')
api.add_resource(chat, '/chat/<string:chatID>')

@app.route("/")
@app.route("/home", methods=["POST", "GET"])
def home():
    return render_template("home.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        uid = request.form["username"]
        pw = request.form["password"]
        name = request.form["Full Name"]
        email = request.form["email"]
        DOB = request.form["DOB"]
        role = request.form["role"]
        admin = request.form["admin"]

        userRef = db.collection(u'users')
        userDocs = (userRef.where(u'username', u'==', uid).where(u'password', u'==', pw)).stream()

        for user in userDocs:
            userData[user.id] = user.to_dict()

        if len(userData) != 0:
            return redirect(url_for("failedLoginSignup"))

        else:
            session["uid"] = uid
            session["pw"] = pw
            session["name"] = name
            session["email"] = email
            session["DOB"] = DOB
            session["role"] = role
            session["admin"] = admin
            session["doctors"] = " "
            session["patients"] = " "
            session["nurses"] = " "

            user = {
                    "username": uid,
                    "password": pw,
                    "name": name,
                    "email": email,
                    "DOB": DOB,
                    "role": role,
                    "admin": admin,
                    "doctors": "",
                    "patients": "",
                    "nurses": "",
                }

            holder = userRef.add(user)

            return redirect(url_for("dashboard"))
    else:
        if "uid" in session and "pw" in session:
            return redirect(url_for("dashboard"))
            
        return render_template("signup.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        uid = request.form["username"]
        pw = request.form["password"]
        session["uid"] = uid
        session["pw"] = pw

        userData = {}
        singleUserData = {}
        userRef = db.collection(u'users')
        userDocs = (userRef.where(u'username', u'==', uid).where(u'password', u'==', pw)).stream()

        for user in userDocs:
            userData[user.id] = user.to_dict()

        if len(userData) != 1:
            session.pop("uid", None)
            session.pop("pw", None)
            return redirect(url_for("failedLoginSignup"))

        else:
            singleUserData = list(userData.values())[0]
            
            session["name"] = singleUserData["name"]
            session["email"] = singleUserData["email"]
            session["DOB"] = singleUserData["DOB"]
            session["role"] = singleUserData["role"]
            session["admin"] = singleUserData["admin"]
            session["doctors"] = singleUserData["doctors"]
            session["patients"] = singleUserData["patients"]
            session["nurses"] = singleUserData["nurses"]

            return redirect(url_for("dashboard"))
    else:
        if "uid" in session and "pw" in session:
            return redirect(url_for("dashboard"))

        return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("uid", None)
    session.pop("pw", None)
    return redirect(url_for("login"))

@app.route("/failedLoginSignup", methods=["POST", "GET"])
def failedLoginSignup():
    return render_template("failedLoginSignup.html")

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
        uid = session["uid"]
        pw = session["pw"]
        name = session["name"]
        email = session["email"]
        DOB = session["DOB"]
        role = session["role"]
        admin = session["admin"]
        doctors = session["doctors"]
        patients = session["patients"]
        nurses = session["nurses"]

        deviceData = {}
        singleDeviceData = {}
        deviceRef = db.collection(u'devices')
        deviceDocs = deviceRef.where(u'patientName', u'==', uid).stream()

        for device in deviceDocs:
            deviceData[device.id] = device.to_dict()

        if len(list(deviceData.values())):
            singleDeviceData = list(deviceData.values())[0]
            
            session["deviceName"] = singleDeviceData["deviceName"]
            session["deviceType"] = singleDeviceData["deviceType"]
            session["manufacturer"] = singleDeviceData["manufacturer"]
            session["patientName"] = singleDeviceData["patientName"]
            session["results"] = singleDeviceData["results"]

            deviceName = session["deviceName"]
            deviceType = session["deviceType"]
            manufacturer = session["manufacturer"]
            patientName = session["patientName"]
            results = session["results"]

            return render_template("dashboard.html", username = uid, password = pw, 
            name = name, email = email, DOB = DOB, role = role, admin = admin, 
            doctors = doctors, patients = patients, nurses = nurses,
            deviceName = deviceName, deviceType = deviceType, manufacturer = manufacturer, 
            patientName = patientName, results = results)

        else:
            return render_template("dashboard.html", username = uid, password = pw, 
            name = name, email = email, DOB = DOB, role = role, admin = admin, 
            doctors = doctors, patients = patients, nurses = nurses)


@app.route("/chatWindow", methods=["POST", "GET"])
def chatWindow():
    chatPartner = " "
    recievedMsg = " "
    sentMsg = " "
    source = session["uid"]
    if request.method == "POST":
        recievedMsg = " "
        chatPartner = request.form["chatPartner"]
        sentMsg = request.form["sentMsg"]
        session["chatPartner"] = chatPartner
        session["sentMsg"] = sentMsg
        session["recievedMsg"] = recievedMsg

        chatData = {}
        singleChatData = {}
        chatRef = db.collection(u'chats')
        chatDocs = chatRef.where(u'dest', u'==', chatPartner).stream()

        for chat in chatDocs:
            chatData[chat.id] = chat.to_dict()

        if len(list(chatData.values())):
            singleChatData = list(chatData.values())[0]

        if len(singleChatData) == 4:
            session["recievedMsg"] = singleChatData["recievedMsg"]

        chatPartner = session["chatPartner"]
        sentMsg = session["sentMsg"]
        source = session["uid"]

        chats = {
                "dest": chatPartner,
                "source": source,
                "sentMsg": sentMsg,
                "recievedMsg": recievedMsg
            }

        holder = chatRef.add(chats)

        return render_template("chatWindow.html", chatPartner = chatPartner, sentMsg = sentMsg, recievedMsg = recievedMsg, source = source)

    else:
        return render_template("chatWindow.html", chatPartner = chatPartner, sentMsg = sentMsg, source = source)


@app.route("/updateDevice", methods=["POST", "GET"])
def updateDevice():
    if request.method == "POST":
        deviceName = request.form["dName"]
        deviceType = request.form["dType"]
        manufacturer = request.form["manufacturer"]
        patientName = request.form["pName"]
        results = request.form["results"]
        session["deviceName"] = deviceName
        session["deviceType"] = deviceType
        session["manufacturer"] = manufacturer
        session["patientName"] = patientName
        session["results"] = results

        deviceRef = db.collection(u'devices')

        devices = {
                "deviceName": deviceName,
                "deviceType": deviceType,
                "manufacturer": manufacturer,
                "patientName": patientName,
                "results": results
            }

        holder = deviceRef.add(devices)

        return redirect(url_for("dashboard"))
    else:
        return render_template("updateDevice.html")

@app.route("/updateDoctors", methods=["POST", "GET"])
def updateDoctors():
    if request.method == "POST":
        doctors = request.form["doctors"]
        session["doctors"] = doctors
        uid = session["uid"]

        userRef = db.collection(u'users')
        userDocs = userRef.where(u'username', u'==', uid).stream()

        for user in userDocs:
            userData[user.id] = user.to_dict()

        for key, value in userData.items() :
            userID = key

        print(userID)

        holder = userRef.document(userID)
        holder.update({u'doctors': doctors})

        return redirect(url_for("dashboard"))

    else:
        return render_template("updateDoctors.html")

@app.route("/updateNurses", methods=["POST", "GET"])
def updateNurses():
    if request.method == "POST":
        nurses = request.form["nurses"]
        session["nurses"] = nurses
        uid = session["uid"]

        userRef = db.collection(u'users')
        userDocs = userRef.where(u'username', u'==', uid).stream()

        for user in userDocs:
            userData[user.id] = user.to_dict()

        for key, value in userData.items() :
            userID = key

        print(userID)

        holder = userRef.document(userID)
        holder.update({u'nurses': nurses})

        return redirect(url_for("dashboard"))

    else:
        return render_template("updateNurses.html")

@app.route("/updatePatients", methods=["POST", "GET"])
def updatePatients():
    if request.method == "POST":
        patients = request.form["patients"]
        session["patients"] = patients
        uid = session["uid"]

        userRef = db.collection(u'users')
        userDocs = userRef.where(u'username', u'==', uid).stream()

        for user in userDocs:
            userData[user.id] = user.to_dict()

        for key, value in userData.items() :
            userID = key

        print(userID)

        holder = userRef.document(userID)
        holder.update({u'patients': patients})

        return redirect(url_for("dashboard"))
        
    else:
        return render_template("updatePatients.html")

if __name__ == '__main__':
    app.run(debug = True, threaded = True)
