from contextlib import contextmanager
import os
from compose.cli.command import project_from_options
from yaml import dump
from PyCrane.command.Foreman import Foreman
from PyCrane.model.Instance import Instance


class ComposeForeman(Foreman):

    _compose_file_name_template = 'compose_{0}.yml'

    _instance_repr_fields = (('image', 'image'),
                             ('command', 'command'))

    @contextmanager
    def _get_project(self, host):
        try:
            compose_file_path = self._dump_compose_file(host)
            self._apply_environ(host)
            yield project_from_options('./', {'--file': [compose_file_path]})
        except Exception as exc:
            raise
        finally:
            self._clean_environ()

    def _apply_environ(self, host):
        os.environ['DOCKER_HOST'] = host.get_socket()
        # os.environ['DOCKER_CERT_PATH']
        # os.environ['DOCKER_TLS_VERIFY']

    def _clean_environ(self):
        del(os.environ['DOCKER_HOST'])  # Keep previous value ?

    def _dump_compose_file(self, host):
        compose_repr = {}
        host_compose_file_path = self._compose_file_name_template.format(host.get_name())

        for instance in self._instances.find_by_host(host):
            compose_repr[instance.get_name()] = self._instance_repr(instance)

        with open(host_compose_file_path, 'w') as compose_file:
            dump(compose_repr, compose_file)

        return host_compose_file_path

    def _instance_repr(self, instance: Instance):
        instance_repr = {}
        for repr_name, field_name in self._instance_repr_fields:
            field_value = getattr(instance, "get_{0}".format(field_name))()
            if field_value:
                instance_repr[repr_name] = field_value

        if instance.get_enabled():
            instance_repr['restart'] = 'always'

        return instance_repr

    def run(self, instance: Instance):
        """
        TODO: Si tourne deja, raise, sinon, get_project.up
        :param instance:
        :return:
        """
        host = self._hosts.find_one_by_name(instance.get_host())
        with self._get_project(host) as project:
            project.up([instance.get_name()], detached=True)  # detached: création d'un démon ?

    def stop(self, instance: Instance):
        host = self._hosts.find_one_by_name(instance.get_host())
        with self._get_project(host) as project:
            project.stop([instance.get_name()])

    def up(self):
        for host in self._hosts:
            with self._get_project(host) as project:
                project.up(detached=True)
