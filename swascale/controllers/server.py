from flask import Blueprint, request, Response
import json
from bson.json_util import dumps
from swascale.domain import db

from swascale.domain.server import Server
from swascale.utils.tasks import create_vm

server = Blueprint('server', 'server')


@server.route('', methods=['GET'])
def index():
    response = Response(
        dumps(db.servers.find()),
        status=200,
        mimetype='application/json'
        )
    return response


@server.route('', methods=['POST'])
def create():
    create_vm.delay(request.get_json())
    return 'created'


@server.route('<uid>', methods=['DELETE'])
def delete(uid):
    Server.delete(uid)
    return 'deleted'


@server.route('/truncate', methods=['DELETE'])
def truncate():
    Server.truncate()
    return 'truncate'
