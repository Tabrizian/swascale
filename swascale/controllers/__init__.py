from flask import Flask

from swascale.controllers.server import server

app = Flask(__name__)
app.register_blueprint(server, url_prefix='/server')
