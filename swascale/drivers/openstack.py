from .base import Driver
from config import cfg

import os_client_config
import novaclient
import click


class OpenStackProvider(Driver):
    name = 'openstack'

    def __init__(self, region):
        try:
            os_cfg = cfg['openstack']

            credentials = {
                "version": os_cfg['OS_COMPUTE_API_VERSION'],
                "auth_url": os_cfg['OS_AUTH_URL'],
                "username": os_cfg['OS_USERNAME'],
                "password": os_cfg['OS_PASSWORD'],
                "project_name": os_cfg['OS_PROJECT_NAME'],
                "region_name": region
            }

            self.nova = os_client_config.make_client('compute', **credentials)
            self.glance = os_client_config.make_client('image', **credentials)
            self.neutron = os_client_config.make_client('network',
                                                        **credentials)
        except FileNotFoundError:
            click.secho('OpenStack configuration not found.', fg='red')
            exit()

    def create_server(self, image_name, flavor_name, instance_name,
                      network_labels, key_name=None):
        image = self.glance.images.find(name=image_name)
        flavor = self.nova.flavors.find(name=flavor_name)

        nics = []
        for network_label in network_labels:
            net = self.neutron.list_networks(name=network_label)
            nics.append({'net-id': net['networks'][0]['id']})

        instance = self.nova.servers.create(
            name=instance_name,
            image=image,
            flavor=flavor,
            nics=nics,
            key_name=key_name
            )

        return instance.id

    def delete_server(self, instance_id):
        try:
            self.nova.servers.get(instance_id).delete()
        except novaclient.exceptions.NotFound:
            click.secho(
                'Server has been deleted from other sources', fg='yellow')

    def ips(self, instance_id):
        return self.nova.servers.ips(instance_id)
