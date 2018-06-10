import json

from swascale.controllers import celery
from swascale.domain.server import Server


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
