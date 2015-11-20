from docker import Client


class Command:

    def __init__(self, hosts):
        self._hosts = hosts

    def get_command_result(self, command_name, parameters={}, host=None):
        if host:
            return self._get_command_result_on_host(command_name, host, parameters)
        else:
            response = {}
            for host in self._hosts:
                response[host.get_name()] = self._get_command_result_on_host(command_name, host, parameters)
            return response

    def _get_command_result_on_host(self, command_name, host, parameters):
        client = Client(base_url=host.get_socket())
        return getattr(client, command_name)(parameters)
