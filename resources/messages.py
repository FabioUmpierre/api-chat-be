from models.messages import MessageModel
from models.user import UserModel
from flask import request
from flask_restful import Resource
from time import gmtime, strftime
import datetime

class MessageCrud(Resource):
    
    def post(self, logged_user_id, contact_user_id):
        payload = None
        try:
            payload = request.json
        except:
            return {"error": "invalid JSON body"}, 400

        success = MessageModel.save_message(
            text=payload.get('text'),
            userId=logged_user_id,
            contactUserId=contact_user_id
        )
        if success:
            return {"message": "message was saved"}, 200
        return {"error": "unable to save message"}, 500

    def get(self, logged_user_id, contact_user_id):
        logged_user = UserModel.find_by_id(contact_user_id)

        logged_user_messages = MessageModel.get_messages(
            userId=logged_user_id,
            contactUserId=contact_user_id
        )
        contact_user_messages = MessageModel.get_messages(
            userId=contact_user_id,
            contactUserId=logged_user_id
        )
        if isinstance(logged_user_messages, list) and isinstance(contact_user_messages, list):
            response = [
                {
                    **x.json(), 
                    'sentByUserId': logged_user_id, 
                    'imageUrl': logged_user.imageUrl
                } 
                for x in logged_user_messages
            ]
            response.extend(
                [
                    {**x.json(), 'sentByUserId': contact_user_id}
                    for x in contact_user_messages
                ]
            )
            response.sort(key=lambda x: datetime.datetime.strptime(
                x['sendTime'], '%Y-%m-%d %H:%M:%S')
            )

            return response
        return {"error": "unable to retrieve messages"}, 500
