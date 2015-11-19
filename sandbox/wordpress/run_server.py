import sys
sys.path.append('../../')

from PyCrane.server.Core import Core
from PyCrane.Supervisor import Supervisor
from sandbox.wordpress.config import wordpress_deployment_config


# TODO: message if not __main__
if __name__ == '__main__':
    core = Core('PyCrane')  # TODO: Configured name
    Supervisor.create_instance(core, wordpress_deployment_config, Supervisor)
    supervisor = Supervisor.get_instance()
    supervisor.build()
    supervisor.start_server()  # TODO: Config server
