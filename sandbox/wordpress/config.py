
HOSTS = {
    'HOST_A': {
        'hostname': 'localhost',
        'socket': 'unix://var/run/docker.sock'
    }
}

APPS = {
    'WORDPRESS': {
        'image': 'TODO',
        # TODO: methode de deploiement
    }
}

wordpress_deployment_config = {
    'HOSTS': HOSTS,
    'APPS': APPS
}
