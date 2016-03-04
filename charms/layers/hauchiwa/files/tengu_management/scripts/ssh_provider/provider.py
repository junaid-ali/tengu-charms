#!/usr/bin/python3
# pylint: disable=C0111,c0321,c0301,c0325
#
""" deploys a tengu env on a general ssh reachable cluster"""
import yaml


class ProviderException(Exception):
    pass


class SSHProvider(object):
    def __init__(self, global_conf):
        self.global_conf = global_conf

    def get(self, env_conf):
        return SSHEnv(self.global_conf, env_conf)

    def create_from_bundle(self, env_conf, bundle):
        env = self.get(env_conf)
        env.create(bundle)
        return env


class SSHEnv(object):
    def __init__(self, global_conf, env_conf):
        self.bundle_path = "{}/bundle.yaml".format(env_conf.dir)

        self.global_conf = global_conf
        self.env_conf = env_conf

    def create(self, bundle):
        print('Creating Tengu SSH environment...')
        with open("{}/bundle.yaml".format(self.env_conf.dir), 'w') as outfile:
            outfile.write(yaml.dump(bundle, default_flow_style=True))

    def renew(self, hours):
        print('Renew unnecessary in SSH environment...')

    def destroy(self):
        # TODO remove juju installation on SSH nodes
        print('Removing Juju environment from nodes...')

    @property
    def machines(self):
        try:
            return get_machines_from_bundle(yaml.load(self.bundle_path))
        except IOError:
            raise ProviderException('Bundle not found')

    @property
    def status(self):
        machines_list = self.machines();
        for machine in machines_list:
            print('')
        return 'TODO Status'


def get_machines_from_bundle(bundle):
    machines = bundle.get('machines')
    machines_list = list()
    if not machines: raise Exception('Could not find machines item in bundle.')
    if not len(machines) > 0: raise Exception('There has to be at least 1 machine specified')
    for m_id in range(len(machines)):
        if not machines.get(str(m_id)): raise Exception(
            'machine {} not found while number of machines is {}.'.format(m_id, len(machines)))
        constraints = machines[str(m_id)].get('constraints').split()
        for constraint in constraints:
            if constraint.startswith('host='):
                machines_list.append(constraint.split('=')[1])
    return machines_list
