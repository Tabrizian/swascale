from flask import Blueprint, request, Response
import json
from bson.json_util import dumps
from swascale.domain import db

from swascale.domain.server import Server

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


@server.route('<uid>', methods=['DELETE'])
def delete(uid):
    Server.delete(uid)
    return 'deleted'


@server.route('/truncate', methods=['DELETE'])
def truncate():
    Server.truncate()
    return 'truncate'
