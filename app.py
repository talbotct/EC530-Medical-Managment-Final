from flask import Flask, redirect, render_template, request, session
from flask_restful import Resource, Api, reqparse

from users import *
from devices import *
from chats import *

app = Flask(__name__, template_folder = "Template")
api = Api(app)
app.config['SECRET_KEY'] = 'secret'

@app.route("/")
@app.route("/home")
def home():
    return render_template("base.html")

api.add_resource(userList, '/user/')
api.add_resource(user, '/user/<string:userID>')
api.add_resource(deviceList, '/device/')
api.add_resource(device, '/device/<string:deviceID>')
api.add_resource(chatList, '/chat/')
api.add_resource(chat, '/chat/<string:chatID>')

if __name__ == '__main__':
    app.run()