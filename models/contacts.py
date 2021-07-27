from . import db
from models.user import UserModel


class ContactsModel(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    contactUserId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, userId, contactUserId):
        self.userId = userId
        self.contactUserId = contactUserId

    def json(self):
        return {
            k: str(v) for k, v in self.__dict__.items()
            if k != '_sa_instance_state'
        }

    @classmethod
    def select_all_user_contacts(cls, user_id):
        result = result = db.session.query(
            ContactsModel, UserModel
        ).join(
            UserModel, ContactsModel.contactUserId == UserModel.id
        ).filter(
            ContactsModel.userId == user_id
        ).all()
        response = [{
            'id': x.ContactsModel.contactUserId,
            'name': x.UserModel.name,
            'imageUrl': x.UserModel.imageUrl,
        } for x in result]
        return response

    @classmethod
    def find_contact(cls, id):
        return cls.query.filter_by(id=id).first() or None

    def save_contact(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_contact(cls, userId, contactUserId):
        contact_row = cls.query.filter(
            ContactsModel.userId == userId,
            ContactsModel.contactUserId == contactUserId
        ).first()
        if contact_row:
            db.session.delete(contact_row)
            db.session.commit()
            return True

    def verify_chat_exists(field1, field2):
        result = db.session.query(
            ContactsModel
        ).filter(
            ContactsModel.userId == field1, ContactsModel.contactUserId == field2
        ).all()
        if len(result) > 0:
            return {"message": "contact already exists"}
