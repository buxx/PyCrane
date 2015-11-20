
IMAGES = [
    ('debian:jessie', ),  # TODO: un exemple de hub personalisé
    ('wordpress', )
]

HOSTS = {
    'HOST_A': {
        'hostname': 'localhost',
        'socket': 'unix://var/run/docker.sock',
        'images': IMAGES
    },
    'HOST_B': {
        'hostname': 'localhost',
        'socket': 'unix://var/run/docker.sock',
        'images': IMAGES
    }
}

APPS = {
    'WORDPRESS': {
        'image': 'TODO',
        # TODO: methode de deploiement
    },
    'MYSQL': {
        'image': 'TODO',
        # TODO: methode de deploiement
    }
}

wordpress_deployment_config = {
    'HOSTS': HOSTS,
    'APPS': APPS
}
