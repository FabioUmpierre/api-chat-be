from flask_restful import Resource, reqparse
from flask import request
from models.contacts import ContactsModel
from . import db




class MessageModel2(db.Model):
    __tablename__ = 'message2'
    id = db.Column(db.Integer, primary_key=True)
    contactRelationshipId = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    text = db.Column(db.String(40))
    # TODO: change to datetime
    sentAt = db.Column(db.String(100))

    def json(self):
        return {
            'text': self.text,
            'sentAt': self.sentAt
        }

    @classmethod
    def save_message(cls, text: str, userId: int, contactUserId: int):
        # sentAt = datetime.now()
        contact_relationship = ContactsModel.get_relationship(userId, contactUserId)
        if contact_relationship:
            new_message = cls(
                contactRelationshipId=contact_relationship.id,
                text=text,
                sentAt='hoje'
            )
            db.session.add(new_message)
            db.session.commit()
            return True
        return False

    @classmethod
    def get_messages(cls, userId: int, contactUserId: int):
        contact_relationship = ContactsModel.get_relationship(userId, contactUserId)
        if contact_relationship:
            return cls.query.filter_by(
                contactRelationshipId=contact_relationship.id
            ).all()
        return False



class MessageModel(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    loggedId = db.Column(db.Integer, db.ForeignKey('contacts.userId'))
    contactMessageId = db.Column(db.Integer, db.ForeignKey('contacts.contactUserId'))
    text = db.Column(db.String(40))

    def __init__(self, loggedId, contactMessageId, text):
        self.loggedId = loggedId
        self.contactMessageId = contactMessageId
        self.text = text

    def json(self):
        return {
            "text": self.text
        }

    def save_message(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def show_message(cls, loggedId, contactMessageId):
        return cls.query.filter_by(
            loggedId=loggedId,
            contactMessageId=contactMessageId
        ).all()


class receive_attribute(Resource):
    atributes = reqparse.RequestParser()
    atributes.add_argument('text', type=str, required=True,
                           help="The field 'text' cannot be left blank.")


class MessageCrud(Resource):
    # def get(self, loggedUserId: int, contactMessageId: int):
    #     '''
    #     Returns a list of messages of the conversation between the logged user 
    #     and his contact.
    #     '''
    #     messages = MessageModel.show_message(loggedUserId, contactMessageId)
    #     if messages:
    #         return [x.json() for x in messages]

    #     return {'message': 'message not found.'}, 404

    # def post(self, loggedId, contactMessageId):
    #     dados = receive_attribute.atributes.parse_args()
    #     message = MessageModel(loggedId, contactMessageId, **dados)
    #     message.save_message()
    #     return 200

    def post(self, loggedUserId, contactUserId):
        payload = None
        try:
            payload = request.json
        except:
            return {"error": "invalid JSON body"}, 400

        success = MessageModel2.save_message(
            text=payload.get('text'),
            userId=loggedUserId,
            contactUserId=contactUserId
        )
        if success:
            return {"message": "message was saved"}, 200
        return {"error": "unable to save message"}, 500

    def get(self, loggedUserId, contactUserId):
        messages_list = MessageModel2.get_messages(
            userId=loggedUserId,
            contactUserId=contactUserId
        )
        if isinstance(messages_list, list):
            response = [x.json() for x in messages_list]
            return response, 200
        return {"error": "unable to save message"}, 500