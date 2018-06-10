import json

from swascale.controllers import celery


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
                {'targets': targets, 'labels': {'cluster': str(cluster)}})
            json.dump(prometheusTargets, outfile)
        except ValueError:
            prometheusTargets = []
            prometheusTargets.append(
                {'targets': targets, 'labels': {'cluster': str(cluster)}})
            json.dump(prometheusTargets, outfile)