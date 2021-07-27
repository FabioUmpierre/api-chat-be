from flask_restful import Resource, reqparse
from models.contacts import ContactsModel


class ContactSearch(Resource):
    def get(self, user_id):
        result = ContactsModel.select_all_user_contacts(user_id)
        return result


class ContactCreate(Resource):
    def delete(self, userId, contactUserId):
        deleted = ContactsModel.delete_contact(userId, contactUserId)
        deleted_user_contact = ContactsModel.delete_contact(
            contactUserId, userId)
        if deleted or deleted_user_contact:
            return {'message': 'contact relationship deleted'}
        return {'message': 'contact not found.'}, 404

    def post(self, userId, contactUserId):
        result = ContactsModel.verify_chat_exists(userId, contactUserId)
        if result:
            return result, 400

        contact = ContactsModel(userId, contactUserId)
        contact.save_contact()

        result = ContactsModel.verify_chat_exists(contactUserId, userId)
        if result:
            return result

        contact = ContactsModel(contactUserId, userId)
        contact.save_contact()
        return {'message': 'contact added is succefully!'}
