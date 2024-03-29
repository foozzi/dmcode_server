from celery import Celery
from dmcode_server import create_app
from dmcode_server import tasks

def make_celery(app):
    # set redis url vars
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = app.config['CELERY_BROKER_URL']
    # create context tasks in celery
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    """uncomment for non-pereodical call tasks"""
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = create_app()
celery = make_celery(app)
