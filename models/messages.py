from . import db


class MessageModel(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    loggedId = db.Column(db.Integer, db.ForeignKey('contacts.userId'))
    contactMessageId = db.Column(db.Integer, db.ForeignKey('contacts.contactUserId'))
    text = db.Column(db.String(40))
