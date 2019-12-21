from sqlalchemy.ext.hybrid import hybrid_property
from dmcode_server import db

class Rooms(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

class Editors(db.Model):
    __tablename__ = 'editors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    token = db.Column(db.String(40), nullable=False)
    is_owner = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    createtime = db.Column(db.Integer, nullable=False)

class Invites(db.Model):
    __tablename__ = 'edit_invites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
