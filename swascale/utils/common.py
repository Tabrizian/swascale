from swascale.domain.server import Server
from config import cfg


def translate_id(id):
    ips = []
    server = Server(_id=_id)
    network_interfaces = server.ips
    for nic in network_interfaces:
        ips.append(network_interfaces[nic][0]['addr'])

    return ips


def id_to_swarm(id):
    ip = translate_id(id)[0]
    return ip + ':' + cfg.docker['SWARM_PORT']