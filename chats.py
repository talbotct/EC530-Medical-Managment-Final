from flask import Flask, jsonify, abort
from flask_restful import Resource, Api, reqparse
import os
from google.cloud import firestore

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ttaylor-med-api-3285443a6f89.json'

db = firestore.Client()
chatRef = db.collection(u'chats')

chatDocs = chatRef.stream()
chats = {}
i = 0

for chat in chatDocs:
    #print(f'{device.id} => {device.to_dict()}')
    chats[chat.id] = chat.to_dict()
    i = i + 1

chatPostArgs = reqparse.RequestParser()
chatPostArgs.add_argument("source", type = str, required = True)
chatPostArgs.add_argument("dest", type = str, required = True)
chatPostArgs.add_argument("sessionID", type = str, required = True)
chatPostArgs.add_argument("msgID", type = str, required = True)
chatPostArgs.add_argument("timestamp", type = str, required = True)
chatPostArgs.add_argument("msgContent", type = str, required = True)


chatPutArgs = reqparse.RequestParser()
chatPutArgs.add_argument("source", type = str)
chatPutArgs.add_argument("dest", type = str)
chatPutArgs.add_argument("sessionID", type = str)
chatPutArgs.add_argument("msgID", type = str)
chatPutArgs.add_argument("timestamp", type = str)
chatPutArgs.add_argument("msgContent", type = str)


class chatList(Resource):
    def get(self):
        return chats

    #POST
    def post(self):
        args = chatPostArgs.parse_args()

        chats = {
                "source": args["source"],
                "dest": args["dest"],
                "sessionID": args["sessionID"],
                "msgID": args["msgID"],
                "timestamp": args["timestamp"],
                "msgContent": args["msgContent"]
            }
            
        #POSTS to google firestore database
        holder = chatRef.add(chats)     

        return chats

class chat(Resource):
    #GET
    def get(self, chatID):
        return chats[chatID]

    #PUT
    def put(self, chatID):
        args = chatPutArgs.parse_args()

        if chatID not in chats:
            abort(404, "chatID does not exist")

        else:
            if(args['source']):
                chats[chatID]['source'] = (args['source'])
                holder = chatRef.document(chatID)
                holder.update({u'source': args['source']})
            if(args['dest']):
                chats[chatID]['dest'] = (args['dest'])
                holder = chatRef.document(chatID)
                holder.update({u'dest': args['dest']})
            if(args['sessionID']):
                chats[chatID]['sessionID'] = (args['sessionID'])
                holder = chatRef.document(chatID)
                holder.update({u'sessionID': args['sessionID']})
            if(args['msgID']):
                chats[chatID]['msgID'] = (args['msgID'])
                holder = chatRef.document(chatID)
                holder.update({u'msgID': args['msgID']})
            if(args['timestamp']):
                chats[chatID]['timestamp'] = (args['timestamp'])
                holder = chatRef.document(chatID)
                holder.update({u'timestamp': args['timestamp']})
            if(args['msgContent']):
                chats[chatID]['msgContent'] = (args['msgContent'])
                holder = chatRef.document(chatID)
                holder.update({u'msgContent': args['msgContent']})
                
        return chats[chatID]

    #DELETE
    def delete(self, chatID):
        if chatID not in chats:
            abort(404, "chatID does not exist")
    
        else:
            holder = chatRef.document(chatID).delete()

            del chats[chatID]
        
        return chats

#if __name__ == '__main__':
    #app.run()