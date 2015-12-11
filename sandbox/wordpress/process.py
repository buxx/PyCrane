from PyCrane.process import Instanciate


class WordpressInstanciate(Instanciate):

    def update_instance(self, instance):
        ports = instance.get_ports() or []

        # Determine port with real context
        ports.append('8080:80')

        instance.set_ports(ports)
