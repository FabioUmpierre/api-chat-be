from . import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    imageUrl = db.Column(db.String(40))
    userName = db.Column(db.String(40))
    email = db.Column(db.String(40))
    password = db.Column(db.String(40))
    # contacts = db.relationship('Contacts', backref='user', lazy=True)

    def __init__(self, name, imageUrl, userName, email, password):
        self.name = name
        self.imageUrl = imageUrl
        self.userName = userName
        self.email = email
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'imageUrl': self.imageUrl,
            'userName': self.userName,
            'email': self.email
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() or None

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first() or None

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first() or None

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    def update_user(self, **kwargs):
        self.name = kwargs.get('name', self.name)
        self.imageUrl = kwargs.get('imageUrl', self.imageUrl)
        self.userName = kwargs.get('userName', self.userName)
        self.email = kwargs.get('email', self.email)
