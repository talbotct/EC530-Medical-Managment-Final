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

#Working towards web application for chat functionality
#TODO formating application screens

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ttaylor-med-api-3285443a6f89.json'

app = Flask(__name__, template_folder = "templates")
api = Api(app)
app.secret_key = "secret"
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
userID = "tal"

userData = {}

api.add_resource(user, '/user/<string:userID>')
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

        session["uid"] = uid
        session["pw"] = pw
        session["name"] = name
        session["email"] = email
        session["DOB"] = DOB
        session["role"] = role
        session["admin"] = admin

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
        return redirect(url_for("dashboard"))
    else:
        if "uid" in session and "pw" in session:
            return redirect(url_for("dashboard"))

        return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("uid", None)
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
        uid = session["uid"]
        pw = session["pw"]
        name = session["name"]
        email = session["email"]
        DOB = session["DOB"]
        role = session["role"]
        admin = session["admin"]

        return render_template("dashboard.html", username = uid, password = pw, name = name, email = email, DOB = DOB, role = role, admin = admin)

@app.route("/updateDevice", methods=["POST", "GET"])
def updateDevice():
    return render_template("updateDevice.html")

@app.route("/updateDoctors", methods=["POST", "GET"])
def updateDoctors():
    return render_template("updateDoctors.html")

@app.route("/updateNurses", methods=["POST", "GET"])
def updateNurses():
    return render_template("updateNurses.html")

@app.route("/updatePatients", methods=["POST", "GET"])
def updatePatients():
    return render_template("updatePatients.html")

# @app.route("/testCall", methods=["POST", "GET"])
# def testCall():

#     # Using LocalHost for testing after taking down Google Cloud
#     url = "http://127.0.0.1:5000/"

#     # It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
#     myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)
#     #print (myResponse.status_code)

#     # For successful API call, response code will be 200 (OK)
#     if(myResponse.ok):

#         # Loading the response data into a dict variable
#         # json.loads takes in only binary or string variables so using content to fetch binary content
#         # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
#         jData = json.loads(myResponse.content)

#         print("The response contains {0} properties".format(len(jData)))
#         print("\n")
#         for key in jData:
#             print key + " : " + jData[key]
#     else:
#     # If response code is not ok (200), print the resulting http error code with description
#         myResponse.raise_for_status()


#     return render_template("home.html")

if __name__ == '__main__':
    app.run(debug = True, threaded = True)
