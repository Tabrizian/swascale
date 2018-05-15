from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader

import os

from .options import Options
from config import cfg


class Ansible:

    __instance = None

    @staticmethod
    def getInstance():
        if Ansible.__instance is None:
            Ansible()
        return Ansible.__instance

    def __init__(self):
        if Ansible.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Ansible.__instance = self
            ansible_cfg = cfg['ansible']
            self.loader = DataLoader()
            self.passwords = {}
            self.options = Options()
            self.options.become_method = ansible_cfg['BECOME_METHOD']
            self.options.become_user = ansible_cfg['BECOME_USER']
            self.options.become = True
            self.options.private_key_file = ansible_cfg['PRIVATE_SSH_KEY']
            self.options.connection = ansible_cfg['CONNECTION']
            self.options.forks = 1

    def execute_playbook(self, playbook, ips):
        ansible_cfg = cfg['ansible']
        ips.append('')
        self.inventory = InventoryManager(
                loader=self.loader,
                sources=','.join(ips)
                )
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)
        self.passwords = {'become_pass': ansible_cfg['BECOME_PASS']}
        self.options.hostlist = ips
        os.environ['ANSIBLE_CONFIG'] = cfg.ansible['ANSIBLE_CONFIG']
        self.options.extra_vars = None
        self.variable_manager.extra_vars = {}
        pbex = PlaybookExecutor(
                playbooks=['playbooks/' + playbook],
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords
                )
        pbex.run()
