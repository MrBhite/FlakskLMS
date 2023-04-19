from init import db

from sqlalchemy.dialects.mysql import VARCHAR, TEXT, BIGINT, INTEGER, SMALLINT, TINYINT, DECIMAL, FLOAT, DOUBLE, DATETIME, TIMESTAMP, DECIMAL


class User(db.Model):
    __name__ = 'user'
    id = db.Column(db.String(12), primary_key=True)
    password = db.Column(db.String(16))
    introduce = db.Column(db.String(255))
    type = db.Column(db.Integer)


    def __init__(self, uid, password, introduce, type):
        self.id = uid
        self.password = password
        self.introduce = introduce
        self.type = type

