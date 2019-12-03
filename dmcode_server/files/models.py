from sqlalchemy.ext.hybrid import hybrid_property
from dmcode_server import db


class Files(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(), nullable=False)
    filesize = db.Column(db.Integer, nullable=False)
    fileext = db.Column(db.String())
    filecontent = db.Column(db.String())
    filehash = db.Column(db.String(), nullable=False)
    createtime = db.Column(db.Integer)
    fileview = db.Column(db.Integer)

    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'), nullable=False)
    app = db.relationship('Apps', backref=db.backref('files', lazy=True))


class Apps(db.Model):
    __tablename__ = 'apps'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(40), nullable=False)
    createtime = db.Column(db.Integer)
