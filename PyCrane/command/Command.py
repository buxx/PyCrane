from docker import Client


class Command:

    def __init__(self, hosts):
        self._hosts = hosts

    def get_command_result(self, command_name, host, parameters):
        client = Client(base_url=host.get_socket())
        return getattr(client, command_name)(**parameters)
