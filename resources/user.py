from flask_restful import Resource, reqparse


class receive_attribute(Resource):
    atributes = reqparse.RequestParser()
    atributes.add_argument(
        'name', type=str, required=True,
        help="The field 'name' cannot be left blank."
    )
    atributes.add_argument(
        'imageUrl', type=str, required=True,
        help="The field 'imageUrl' cannot be left blank."
    )
    atributes.add_argument(
        'userName', type=str, required=True,
        help="The field 'userName' cannot be left blank."
    )
    atributes.add_argument(
        'email', type=str, required=True,
        help="The field 'email' cannot be left blank."
    )
    atributes.add_argument(
        'password', type=str, required=True,
        help="The field 'password' cannot be left blank."
    )


def is_valid(field):
    return {
        "message": f"the field {field} cannot be left blank"
    }
