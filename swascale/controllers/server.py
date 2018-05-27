from flask import Blueprint, Response
import json
from bson.json_util import dumps

import swascale.model.server as ServerModel


server = Blueprint('server', 'server')


@server.route('/', methods=['GET'])
def index():
    response = Response(
        dumps(ServerModel.Server.objects.values().all()),
        status=200,
        mimetype='application/json'
        )
    return response
