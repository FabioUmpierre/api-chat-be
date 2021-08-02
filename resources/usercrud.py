from flask_restful import Resource
from models.user import UserModel
from flask import request, jsonify


class UserCrud(Resource):
    def get(self, id):
        user = UserModel.find_by_id(id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    def delete(self, id):
        user = UserModel.find_by_id(id)
        if user:
            # TODO: first delete all contact relationaship that uses this user id
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404

    def patch(self, id):
        user_found = UserModel.find_by_id(id)
        if user_found:
            user_found.update_user(**request.json)
            user_found.save_user()
            return user_found.json(), 200

        return jsonify({
            'message': 'Usuário não encontrado'
        }), 404
