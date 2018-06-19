from flask import Blueprint, request, Response
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from swascale.domain import db
from swascale.domain.server import Server
from swascale.utils.tasks import delete_cluster_id, add_cluster_id, create_rule, delete_rule
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


@cluster.route('/<cluster_id>', methods=['GET'])
def show(cluster_id):
    cluster = db.clusters.find_one({'_id': ObjectId(cluster_id)})
    response = Response(
        dumps(cluster),
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
    if 'up' in request.get_json():
        rule = request.json.get('up')
        direction = 'up'
        db.clusters.update_one({'_id': cluster}, {
            '$set': {'up': request.json.get('up')}
            })

    if 'down' in request.get_json():
        rule = request.json.get('down')
        direction = 'down'
        db.clusters.update_one({'_id': cluster}, {
            '$set': {'down': request.json.get('down')}
            })

    add_cluster_id.delay(targets, str(cluster))

    return 'created'


@cluster.route('/<cluster_id>', methods=['POST'])
def update(cluster_id):
    cluster = db.clusters.find_one({'_id': ObjectId(cluster_id)})
    rule = None
    direction = None
    if 'up' in request.get_json():
        rule = request.json.get('up')
        direction = 'up'
        db.clusters.update_one({'_id': ObjectId(cluster_id)}, {
            '$set': {'up': request.json.get('up')}
            })

    if 'down' in request.get_json():
        rule = request.json.get('down')
        direction = 'down'
        db.clusters.update_one({'_id': ObjectId(cluster_id)}, {
            '$set': {'down': request.json.get('down')}
            })

    create_rule.delay(rule, str(cluster['_id']), direction)

    return 'updated'


@cluster.route('/<cluster_id>', methods=['DELETE'])
def delete(cluster_id):
    cluster = db.clusters.find_one({'_id': ObjectId(cluster_id)})
    for vm in cluster['vms']:
        vm = Server(_id=vm['_id'])
        vm.swarm_leave()

    delete_cluster_id.delay(cluster_id)
    delete_rule.delay(cluster_id)
    db.clusters.remove({'_id': ObjectId(cluster_id)})
    return 'cluster removed'
