from flask_restful import Resource, reqparse
from models.contacts import ContactsModel
from . import db
from time import gmtime, strftime
import datetime


class MessageModel(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    contactRelationshipId = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    text = db.Column(db.String(40))
    # TODO: change to datetime
    sendTime = db.Column(db.String(100))

    def json(self):
        return {
            'text': self.text,
            'sendTime': self.sendTime
        }

    @classmethod
    def save_message(cls, text: str, userId: int, contactUserId: int):
        contact_relationship = ContactsModel.get_relationship(
            userId, contactUserId)
        if contact_relationship:
            new_message = cls(
                contactRelationshipId=contact_relationship.id,
                text=text,
                sendTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            db.session.add(new_message)
            db.session.commit()
            return True
        return False

    @classmethod
    def get_messages(cls, userId: int, contactUserId: int):
        contact_relationship = ContactsModel.get_relationship(
            userId, contactUserId)
        if contact_relationship:
            return cls.query.filter_by(
                contactRelationshipId=contact_relationship.id
            ).all()
        return False


class receive_attribute(Resource):
    atributes = reqparse.RequestParser()
    atributes.add_argument('text', type=str, required=True,
                           help="The field 'text' cannot be left blank.")


