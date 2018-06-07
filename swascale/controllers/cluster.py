from flask import Blueprint, request, Response
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from swascale.domain import db
from swascale.domain.server import Server
import json
from config import cfg

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
    targets = []
    vm_manager = None
    for vm in request.json.get('vms'):
        if vm['role'] == 'manager':
            vm_manager = vm
            break
    server = Server(_id=vm_manager['_id'])
    server.swarm_init()
    targets.append(server.ips[server.networks[0]][0]['addr'] + ':' +
                   cfg.prometheus['PROMETHEUS_PORT'])

    for vm in request.json.get('vms'):
        if vm['_id'] != vm_manager['_id']:
            if vm['role'] == 'manager':
                manager = Server(_id=vm['_id'])
                manager.swarm_join_manager(server)
                targets.append(manager.ips[manager.networks[0]][0]['addr'] +
                               ':' + cfg.prometheus['PROMETHEUS_PORT'])
            elif vm['role'] == 'worker':
                worker = Server(_id=vm['_id'])
                worker.swarm_join_worker(server)
                targets.append(worker.ips[worker.networks[0]][0]['addr'] +
                               ':' + cfg.prometheus['PROMETHEUS_PORT'])
    cluster = db.clusters.insert({'vms': request.json.get('vms')})

    with open('config/targets.json', 'r+') as outfile:
        try:
            prometheusTargets = json.load(outfile)
            outfile.seek(0)
            prometheusTargets.append(
                {'targets': targets, 'labels': {'cluster': str(cluster)}})
            json.dump(prometheusTargets, outfile)
        except ValueError:
            prometheusTargets = []
            prometheusTargets.append(
                {'targets': targets, 'labels': {'cluster': str(cluster)}})
            json.dump(prometheusTargets, outfile)

    return 'created'


@cluster.route('/<cluster_id>', methods=['POST'])
def update():
    return 'created'
