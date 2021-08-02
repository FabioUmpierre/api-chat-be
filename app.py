from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.usersearch import UserSearch
from resources.userlist import UserList
from resources.usercrud import UserCrud
from resources.contacts import ContactCreate, ContactSearch
from resources.messages import MessageCrud
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


@app.before_first_request
def create_db():
    db.create_all()


api.add_resource(UserList, '/user')
api.add_resource(UserCrud, '/user/<int:id>')
api.add_resource(UserSearch, '/user/search/<string:name>')
api.add_resource(ContactSearch, '/user/<int:user_id>/contacts')
api.add_resource(
    ContactCreate, '/user/<int:userId>/contact/<int:contactUserId>')
api.add_resource(
    MessageCrud, '/user/<int:logged_user_id>/contacts/<int:contact_user_id>/messages')

db.init_app(app)

if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
        dbapi_con.execute('pragma foreign_keys=ON')

    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)

if __name__ == '__main__':
    app.run(debug=True)
