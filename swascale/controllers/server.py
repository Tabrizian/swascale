from flask import Blueprint, request, Response
import json
from bson.json_util import dumps

import swascale.model.server as ServerModel
from swascale.domain.server import Server


server = Blueprint('server', 'server')


@server.route('', methods=['GET'])
def index():
    response = Response(
        dumps(ServerModel.Server.objects.values().all()),
        status=200,
        mimetype='application/json'
        )
    return response


@server.route('', methods=['POST'])
def create():
    print(request.json['region'])
    server = Server(
        name=request.json['name'],
        image=request.json['image'],
        networks=request.json['networks'],
        region=request.json['region'],
        driver=request.json['driver'],
        flavor=request.json['flavor'],
        key=request.json['key']
        )
    server.create()
    return 'created'
