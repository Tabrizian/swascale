from ..drivers.base import BaseDriver
from swascale.utils.ansible import Ansible
from . import db
from bson.objectid import ObjectId
import docker

import click
from os import system


class Server:
    def __init__(
            self=None, name=None, image=None,
            flavor=None, region=None, driver=None, networks=None,
            key=None, _id=None
            ):
        if _id is not None:
            server = db.servers.find_one({'_id': ObjectId(_id)})
            self._id = server['uid']
            self.uid = _id
            self.name = server['name']
            self.flavor = server['flavor']
            self.region = server['region']
            self.image = server['image']
            self.networks = server['networks']
            if 'key' in server:
                self.key = server['key']
            self.driver = BaseDriver.get(server['driver'])(server['region'])
        else:
            self._id = None
            self.name = name
            self.flavor = flavor
            self.region = region
            self.image = image
            self.networks = networks
            self.key = key
            self.driver = BaseDriver.get(driver)(region)

    @staticmethod
    def truncate():
        servers = db.servers.find()

        for server in servers:
            driver = BaseDriver.get(server['driver'])(server['region'])
            driver.delete_server(server['_id'])
            click.secho('server => driver: %s, id: %s' %
                        (server['driver'], server['name']),
                        fg="red")
            server.delete()

    def create(self):
        self._id = self.driver.create_server(
            self.image, self.flavor, self.name, self.networks, self.key)

        while self.ips == {}:
            pass

        vm_data = {
            "_id": self._id,
            "name": self.name,
            "flavor": self.flavor,
            "region": self.region,
            "image": self.image,
            "networks": self.networks,
            "ips": self.ips,
            "driver": self.driver.name
            }
        """
        Whether it has key pair or not
        """
        if self.key is not None:
            vm_data['key'] = self.key
        Ansible.getInstance().execute_playbook(
            [self.ips[self.networks[0]][0]['addr']]
        )
        server = db.servers.insert_one({
            'uid': self._id,
            'name': self.name,
            'image': self.image,
            'flavor': self.flavor,
            'networks': self.networks,
            'region': self.region,
            'driver': self.driver.name
        })
        self.uid = server._id

    @staticmethod
    def delete(uid):
            servers = db.servers.find({'_id': ObjectId(uid)})
            driver = BaseDriver.get(servers[0]['driver'])(servers[0]['region'])
            driver.delete_server(servers[0]['uid'])
            db.servers.remove({'_id': ObjectId(uid)})

    @property
    def ips(self):
        return self.driver.ips(self._id)

    def swarm_init(self):
        swarm_client = docker.DockerClient(
            'tcp://' +
            self.ips[self.networks[0]][0] +
            ':' + cfg.docker['API_PORT']
        ).swarm

        swarm_client.init('eth0:' + cfg.docker['SWARM_PORT'],
                          '0.0.0.0:' + cfg.docker['SWARM_PORT'])
        print(swarm_client.attrs['JoinTokens'])
        db.servers.update_one({_id: ObjectId(self.uid)},
                              swarm_client.attrs['JoinTokens'])
