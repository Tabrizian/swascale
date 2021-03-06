from flask import Flask
from config import cfg
from celery import Celery

import importlib


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['swascale.utils.tasks']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL=cfg.celery['CELERY_BROKER_URL'],
    CELERY_RESULT_BACKEND=cfg.celery['CELERY_RESULT_BACKEND']
)

celery = make_celery(app)

from swascale.controllers.server import server
from swascale.controllers.cluster import cluster
from swascale.controllers.alert import alert


app.register_blueprint(server, url_prefix='/api/server')
app.register_blueprint(cluster, url_prefix='/api/cluster')
app.register_blueprint(alert, url_prefix='/alert')
