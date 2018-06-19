import json
import os
import requests

from swascale.controllers import celery
from swascale.domain.server import Server
from swascale.domain import db
from bson.objectid import ObjectId
from config import cfg

from yaml import load, dump


@celery.task
def delete_cluster_id(cluster_id):
    with open('config/targets.json', 'r+') as outfile:
        prometheusTargets = json.load(outfile)
        outfile.seek(0)
        outfile.truncate()
        outfile.seek(0)
        for configuration in prometheusTargets:
            if configuration['labels']['cluster'] == cluster_id:
                prometheusTargets.remove(configuration)
                break

        json.dump(prometheusTargets, outfile)


@celery.task
def add_cluster_id(targets, cluster):
    with open('config/targets.json', 'r+') as outfile:
        try:
            prometheusTargets = json.load(outfile)
            outfile.seek(0)
            prometheusTargets.append(
                {'targets': targets, 'labels': {'cluster': cluster}})
            json.dump(prometheusTargets, outfile)
        except ValueError:
            prometheusTargets = []
            prometheusTargets.append(
                {'targets': targets, 'labels': {'cluster': cluster}})
            json.dump(prometheusTargets, outfile)

@celery.task
def update_targets():
    clusters = db.clusters.find({})
    prometheusTargets = []
    with open('config/targets.json', 'w') as outfile:
        for cluster in clusters:
            targets = []
            for target in cluster['vms']:
                vm = Server(_id=target['_id'])
                targets.append(vm.ips[vm.networks[0]][0]['addr'] + ':' +
                               cfg.prometheus['PROMETHEUS_PORT'])

            prometheusTargets.append(
                {'targets': targets, 'labels': {
                    'cluster': str(cluster['_id'])
                }}
            )

        json.dump(prometheusTargets, outfile)




@celery.task
def create_vm(vm_data):
    server = Server(
        name=vm_data['name'],
        image=vm_data['image'],
        networks=vm_data['networks'],
        region=vm_data['region'],
        driver=vm_data['driver'],
        flavor=vm_data['flavor'],
        key=vm_data['key']
        )
    server.create()

@celery.task
def create_rule(rule, cluster, direction):
    data = {}
    if direction == 'up':
        data = {
            'groups': [
                {
                    'name': 'Scale up',
                    'rules': [
                        {
                            'alert': 'Scale up alert',
                            'expr': rule,
                            'for': '1m'
                        }
                    ]
                }
            ]
        }
    if direction == 'down':
        data = {
            'groups': [
                {
                    'name': 'Scale down',
                    'rules': [
                        {
                            'alert': 'Scale down alert',
                            'expr': rule,
                            'for': '1m'
                        }
                    ]
                }
            ]
        }

    rule_file = open('config/rules/' + cluster + '_' + direction + '.yml', 'w')
    dump(data, rule_file)
    r = requests.post('http://localhost:443/-/reload')
    rule_file.close()


@celery.task
def delete_rule(cluster):
    if os.path.isfile('config/rules/' + cluster + '_up' + '.yml'):
        os.remove('config/rules/' + cluster + '_up' + '.yml')

    if os.path.isfile('config/rules/' + cluster + '_down' + '.yml'):
        os.remove('config/rules/' + cluster + '_down' + '.yml')

    r = requests.post('http://localhost:443/-/reload')


@celery.task
def add_to_cluster(cluster):
    cluster = db.clusters.find_one({'_id': ObjectId(cluster)})
    manager = None
    for vm in cluster['vms']:
        if vm['role'] == 'manager':
            manager = vm

    server = Server(
        name='scaled_vm',
        image='Ubuntu-16-04',
        networks=['ece1548-net'],
        region='CORE',
        driver='openstack',
        flavor='m1.small',
        key='swascale_key'
        )
    server.create()
    manager = Server(_id=manager['_id'])
    server.swarm_join_worker(manager)
    cluster['vms'].append({
        '_id': str(server.uid),
        'role': 'worker'
    })
    cluster = db.clusters.update_one({'_id': cluster['_id']}, {
        '$set': {
            'vms': cluster['vms']
        }
    })

    update_targets()


@celery.task
def remove_from_cluster(cluster):
    cluster = db.clusters.find_one({'_id': ObjectId(cluster)})
    worker = None
    for vm in cluster['vms']:
        if vm['role'] == 'worker':
            worker = vm
            break

    if worker is None:
        cluster['vms'].remove(worker)
        worker = Server(_id=worker['_id'])
        worker.swarm_leave()
        Server.delete(worker.uid)

        cluster = db.clusters.update_one({'_id': cluster['_id']}, {
            '$set': {
                'vms': cluster['vms']
            }
        })

        update_targets()
