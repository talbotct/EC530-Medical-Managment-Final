from flask import Flask, jsonify, abort
from flask_restful import Resource, Api, reqparse
import os
from google.cloud import firestore

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ttaylor-med-api-3285443a6f89.json'

db = firestore.Client()
deviceRef = db.collection(u'devices')

deviceDocs = deviceRef.stream()
devices = {}
i = 0

for device in deviceDocs:
    #print(f'{device.id} => {device.to_dict()}')
    devices[device.id] = device.to_dict()
    i = i + 1

devicePostArgs = reqparse.RequestParser()
devicePostArgs.add_argument("deviceName", type = str, required = True)
devicePostArgs.add_argument("deviceType", type = str, required = True)
devicePostArgs.add_argument("manufacturer", type = str, required = True)
devicePostArgs.add_argument("hospital", type = str, required = True)
devicePostArgs.add_argument("patientName", type = str)
devicePostArgs.add_argument("results", type = str)

devicePutArgs = reqparse.RequestParser()
devicePutArgs.add_argument("deviceName", type = str)
devicePutArgs.add_argument("deviceType", type = str)
devicePutArgs.add_argument("manufacturer", type = str)
devicePutArgs.add_argument("hospital", type = str)
devicePutArgs.add_argument("patientName", type = str)
devicePutArgs.add_argument("results", type = str)

class deviceList(Resource):
    def get(self):
        return devices

    #POST
    def post(self):
        args = devicePostArgs.parse_args()

        devices = {
                "deviceName": args["deviceName"],
                "deviceType": args["deviceType"],
                "manufacturer": args["manufacturer"],
                "hospital": args["hospital"],
                "patientName": args["patientName"],
                "results": args["results"]
            }

        #POSTS to google firestore database
        holder = deviceRef.add(devices)
            
        return devices

class device(Resource):
    #GET
    def get(self, deviceID):
        return devices[deviceID]

    #PUT
    def put(self, deviceID):
        args = devicePutArgs.parse_args()

        if deviceID not in devices:
            abort(404, "DeviceID does not exist")

        else:
            if(args['deviceName']):
                devices[deviceID]['deviceName'] = (args['deviceName'])
                holder = deviceRef.document(deviceID)
                holder.update({u'deviceName': args['deviceName']})
            if(args['deviceType']):
                devices[deviceID]['deviceType'] = (args['deviceType'])
                holder = deviceRef.document(deviceID)
                holder.update({u'deviceType': args['deviceType']})
            if(args['manufacturer']):
                devices[deviceID]['manufacturer'] = (args['manufacturer'])
                holder = deviceRef.document(deviceID)
                holder.update({u'manufacturer': args['manufacturer']})
            if(args['hospital']):
                devices[deviceID]['hospital'] = (args['hospital'])
                holder = deviceRef.document(deviceID)
                holder.update({u'hospital': args['hospital']})
            if(args['patientName']):
                devices[deviceID]['patientName'] = (args['patientName'])
                holder = deviceRef.document(deviceID)
                holder.update({u'patientName': args['patientName']})
            if(args['results']):
                devices[deviceID]['results'] = (args['results'])
                holder = deviceRef.document(deviceID)
                holder.update({u'results': args['results']})

        return devices[deviceID]

    #DELETE
    def delete(self, deviceID):
        if deviceID not in devices:
            abort(404, "DeviceID does not exist")
    
        else:
            holder = deviceRef.document(deviceID).delete()

            del devices[deviceID]
        
        return devices

#if __name__ == '__main__':
    #app.run()