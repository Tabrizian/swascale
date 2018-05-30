from flask import Blueprint, request, Response
import json
from bson.json_util import dumps
from swascale.domain import db

cluster = Blueprint('cluster', 'cluster')


@cluster.route('', methods=['GET'])
def index():
    response = Response(
        dumps(db.clusters.find()),
        status=200,
        mimetype='application/json'
        )
    return response


@cluster.route('', methods=['POST'])
def create():
    print(request.json['vms'])
    return 'created'
