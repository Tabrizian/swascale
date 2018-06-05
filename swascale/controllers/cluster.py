from flask import Blueprint, request, Response
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from swascale.domain import db
from swascale.domain.server import Server

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
    vm_manager = None
    for vm in request.json.get('vms'):
        if vm['role'] == 'manager':
            print(vm)
            vm_manager = vm
            break
    server = Server(_id=vm_manager['_id'])
    server.swarm_init()

    for vm in request.json.get('vms'):
        if vm['_id'] != vm_manager['_id']:
            if vm['role'] == 'manager':
                manager = Server(_id=vm['_id'])
                manager.swarm_join_manager(server)
            elif vm['role'] == 'worker':
                worker = Server(_id=vm['_id'])
                worker.swarm_join_worker(server)
    return 'created'
