from ..drivers.base import BaseDriver

from os import system
from swascale.utils.ansible import Ansible
import click


class Server:
    def __init__(
            self, name, image, flavor, region, driver, networks,
            key=None
            ):
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
        """
        vms = db.vms.all()
        for vm in vms:
            provider = BaseProvider.get(vm['provider'])(vm['region'])
            provider.delete_server(vm['_id'])
            click.secho('server => provider: %s, id: %s' %
                    (vm['provider'], vm['name']),
                    fg="red")
            ips = []
            ips.extend(common.translate_id(vm['name']))
            for ip in ips:
                system("ssh-keygen -f ~/.ssh/known_hosts -R " + ip)
            db.vms.remove(eids=[vm.eid])
        """
        pass

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

    def delete(self):
        self.driver.delete_server(self._id)

    @property
    def ips(self):
        return self.driver.ips(self._id)
