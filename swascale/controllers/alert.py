from flask import Blueprint, request, Response
import json
import re
from config import cfg
from swascale.utils.tasks import add_to_cluster, remove_from_cluster

alert = Blueprint('alert', 'alert')


@alert.route('', methods=['POST'])
def index():
    print(request.get_json())
    cluster = re.search(
        '.*cluster="(.+)".*',
        request.json.get('groupKey').split(':')[1]).group(1)
    direction = re.search(
        '.*alertname="(.+?)".*',
        request.json.get('groupKey').split(':')[1]
        ).group(1)
    print(direction, cluster)
    if direction == 'Scale up alert':
        add_to_cluster.delay(cluster)
    elif direction == 'Scale down alert':
        remove_from_cluster.delay(cluster)
    return 'ok'
