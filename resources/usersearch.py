from flask_restful import Resource
from models.user import UserModel


class UserSearch(Resource):
    def get(self, name):
        user = UserModel.find_by_name(name)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404
