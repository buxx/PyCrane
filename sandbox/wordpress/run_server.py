import sys
sys.path.append('../../')

from PyCrane.server import Supervisor
from sandbox.wordpress.config import wordpress_deployment_config


# TODO: message if not __main__
if __name__ == '__main__':
    supervisor = Supervisor(wordpress_deployment_config)
    supervisor.start_server()
