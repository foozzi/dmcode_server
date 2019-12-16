from dmcode_server import db, celery
from dmcode_server.files.models import Pastes
from time import time

"""Task for delete expired pastes"""
@celery.task()
def expired_paste_cleaner():
    pastes = Pastes.query.filter((int(time())+Pastes.expiretime) <= int(time())).all()
    for paste in pastes:
        for file in paste.files:
            db.session.delete(file)
        db.session.delete(paste)
    db.session.commit()
