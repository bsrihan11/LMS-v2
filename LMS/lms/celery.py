from celery import Celery,Task
from flask import Flask

def make_celery(app:Flask):
    class FlaskTask(Task):

        def __call__(self,*args,**kwargs):
            with app.app_context():
                self.run(*args,**kwargs)

    celery = Celery(app.name,include=['lms.tasks'])
    celery.Task = FlaskTask
    celery.config_from_object(app.config['CELERY_CONFIG'])


    return celery