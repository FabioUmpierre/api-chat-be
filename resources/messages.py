from models.messages import MessageModel
from flask import request
from flask_restful import Resource
from time import gmtime, strftime
import datetime

class MessageCrud(Resource):
    
    def post(self, loggedUserId, contactUserId):
        payload = None
        try:
            payload = request.json
        except:
            return {"error": "invalid JSON body"}, 400

        success = MessageModel.save_message(
            text=payload.get('text'),
            userId=loggedUserId,
            contactUserId=contactUserId
        )
        if success:
            return {"message": "message was saved"}, 200
        return {"error": "unable to save message"}, 500

    def get(self, loggedUserId, contactUserId):
        messages_list = MessageModel.get_messages(
            userId=loggedUserId,
            contactUserId=contactUserId
        )
        reversed_messages_list = MessageModel.get_messages(
            userId=contactUserId,
            contactUserId=loggedUserId
        )
        if isinstance(messages_list, list) and isinstance(reversed_messages_list, list):
            response = [x.json() for x in messages_list]
            response.extend(
                [x.json() for x in reversed_messages_list]
            )
            response.sort(key=lambda x: datetime.datetime.strptime(
                x['sendTime'], '%Y-%m-%d %H:%M:%S'))
            return response
        return {"error": "unable to save message"}, 500
