from flask_restful import Resource
from models.user import UserModel
from resources.user import receive_attribute, is_valid


class UserList(Resource):
    def get(self):
        return [user.json() for user in UserModel.query.all()]

    def post(self):
        payload = receive_attribute.atributes.parse_args()

        if UserModel.find_by_email(payload['email']):
            return {
                "message": "The email '{}' already exists.".format(payload['email'])
            }

        if len(payload['name']) < 4:
            return is_valid('name')

        if len(payload['imageUrl']) < 4:
            return is_valid('imageUrl')

        if len(payload['userName']) < 4:
            return is_valid('userName')

        if len(payload['email']) < 4:
            return is_valid('email')

        if len(payload['password']) < 4:
            return is_valid('password')

        user = UserModel(**payload)
        user.save_user()
        return user.json(), 201
