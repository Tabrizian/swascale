from flask import Flask

from .server import server

app = Flask(__name__)
app.register_blueprint(server)
