from sqlalchemy.ext.hybrid import hybrid_property
from dmcode_server import db


class Files(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(), nullable=False)
    filepath = db.Column(db.String(), default='')
    filesize = db.Column(db.Integer, nullable=False)
    fileext = db.Column(db.String())
    filecontent = db.Column(db.String())
    filehash = db.Column(db.String(), nullable=False)
    hash = db.Column(db.String(), nullable=False)
    createtime = db.Column(db.Integer, nullable=False)
    updatetime = db.Column(db.Integer, nullable=False)
    fileview = db.Column(db.Integer, default=0)

    paste_id = db.Column(db.Integer, db.ForeignKey(
        'pastes.id'), nullable=False)
    paste = db.relationship('Pastes', backref=db.backref('files', lazy=True))


class Pastes(db.Model):
    __tablename__ = 'pastes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(40), nullable=False)
    hash = db.Column(db.String(20), nullable=False)
    expiretime = db.Column(db.Integer, nullable=False)
    createtime = db.Column(db.Integer, nullable=False)
    updatetime = db.Column(db.Integer, nullable=False)
