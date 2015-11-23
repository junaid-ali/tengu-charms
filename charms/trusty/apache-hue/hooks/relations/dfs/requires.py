from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class HdfsRequires(RelationBase):
    scope = scopes.GLOBAL
    auto_accessors = ['host', 'port']

    @hook('{requires:dfs}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        if conv.get_remote('private-address'):
            # this unit's conversation has a port, so
            # it is part of the set of available units
            conv.set_state('hadoop.hdfs.available')


    @hook('{requires:dfs}-relation-{departed,broken}')
    def broken(self):
        conv = self.conversation()
        conv.remove_state('hadoop.hdfs.available')

    @property
    def private_address(self):
        self.conversation().get_remote('private-address')
