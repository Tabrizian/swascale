from flask import Flask

from swascale.controllers.server import server
from swascale.controllers.cluster import cluster
from swascale.controllers.alert import alert

app = Flask(__name__)
app.register_blueprint(server, url_prefix='/server')
app.register_blueprint(cluster, url_prefix='/cluster')
app.register_blueprint(alert, url_prefix='/alert')
