from flask import Flask, jsonify, abort
from flask_restful import Resource, Api, reqparse
import os
from google.cloud import firestore
import threading

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ttaylor-med-api-3285443a6f89.json'

db = firestore.Client()
userRef = db.collection(u'users')

userDocs = userRef.stream()
users = {}
i = 0

for user in userDocs:
    users[user.id] = user.to_dict()
    i = i + 1

callback_done = threading.Event()

def on_snapshot(userSnapshot, changes, read_time):
    for user in userSnapshot:
        print(f'Received user snapshot: {user.id}')
    callback_done.set()

doc_ref = db.collection(u'users')

doc_watch = doc_ref.on_snapshot(on_snapshot)


userPostArgs = reqparse.RequestParser()
userPostArgs.add_argument("name", type = str, required = True)
userPostArgs.add_argument("role", type = str, required = True)
userPostArgs.add_argument("admin", type = str, required = True)
userPostArgs.add_argument("DOB", type = str, required = True)
userPostArgs.add_argument("email", type = str, required = True)
userPostArgs.add_argument("password", type = str, required = True)
userPostArgs.add_argument("doctors", type = str)
userPostArgs.add_argument("nurses", type = str)
userPostArgs.add_argument("patients", type = str)

userPutArgs = reqparse.RequestParser()
userPutArgs.add_argument("name", type = str)
userPutArgs.add_argument("role", type = str)
userPutArgs.add_argument("admin", type = str)
userPutArgs.add_argument("DOB", type = str)
userPutArgs.add_argument("email", type = str)
userPutArgs.add_argument("password", type = str)
userPutArgs.add_argument("doctors", type = str)
userPutArgs.add_argument("nurses", type = str)
userPutArgs.add_argument("patients", type = str)

def getDB(db):
    db = firestore.Client()
    userRef = db.collection(u'users')

    userDocs = userRef.stream()
    users = {}
    i = 0

    for user in userDocs:
        users[user.id] = user.to_dict()
        i = i + 1

class userList(Resource):
    def get(self):
        getDB(db)
        return users

    #POST
    def post(self):
        getDB(db)
        
        args = userPostArgs.parse_args()

        users = {
                "name": args["name"],
                "role": args["role"],
                "admin": args["admin"],
                "DOB": args["DOB"],
                "email": args["email"],
                "password": args["password"],
                "doctors": args["doctors"],
                "nurses": args["nurses"],
                "patients": args["patients"]
            }
            
        #POSTS to google firestore database
        holder = userRef.add(users)        
    
        return users

class user(Resource):
    #GET
    def get(self, userID):
        getDB(db)
        return users[userID]

    #PUT
    def put(self, userID):
        getDB(db)

        args = userPutArgs.parse_args()

        if userID not in users:
            abort(404, "UserID does not exist")

        else:
            if(args['name']):
                users[userID]['name'] = (args['name'])
                holder = userRef.document(userID)
                holder.update({u'name': args['name']})
            if(args['role']):
                users[userID]['role'] = (args['role'])
                holder = userRef.document(userID)
                holder.update({u'role': args['role']})
            if(args['admin']):
                users[userID]['admin'] = (args['admin'])
                holder = userRef.document(userID)
                holder.update({u'admin': args['admin']})
            if(args['DOB']):
                users[userID]['DOB'] = (args['DOB'])
                holder = userRef.document(userID)
                holder.update({u'DOB': args['DOB']})
            if(args['email']):
                users[userID]['email'] = (args['email'])
                holder = userRef.document(userID)
                holder.update({u'email': args['email']})
            if(args['password']):
                users[userID]['password'] = (args['password'])
                holder = userRef.document(userID)
                holder.update({u'password': args['password']})
            if(args['doctors']):
                users[userID]['doctors'] = (args['doctors'])
                holder = userRef.document(userID)
                holder.update({u'doctors': args['doctors']})
            if(args['nurses']):
                users[userID]['nurses'] = (args['nurses'])
                holder = userRef.document(userID)
                holder.update({u'nurses': args['nurses']})
            if(args['patients']):
                users[userID]['patients'] = (args['patients'])
                holder = userRef.document(userID)
                holder.update({u'patients': args['patients']})

        return users[userID]

    #DELETE
    def delete(self, userID):
        getDB(db)

        if userID not in users:
            abort(404, "UserID does not exist")
    
        else:
            holder = userRef.document(userID).delete()

            del users[userID]
        
        return users

#if __name__ == '__main__':
    #app.run()