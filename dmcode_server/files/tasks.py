from celery import Celery
from flask import current_app as app

celery = Celery(app.name)


@celery.task
def paste_cleaner():
    pass
