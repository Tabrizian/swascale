from flask import Blueprint, request, Response
import json
import re
from config import cfg
from swascale.utils.tasks import add_to_cluster

alert = Blueprint('alert', 'alert')


@alert.route('', methods=['POST'])
def index():
    m = re.search('.*cluster="(.+)".*', request.json.get('groupKey').split(':')[1])
    cluster = m.group(1)
    add_to_cluster.delay(cluster)
    return 'ok'
