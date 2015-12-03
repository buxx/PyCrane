HOSTS = [
    {
        'name': 'HOST_A',
        'hostname': 'localhost',
        'socket': 'http+unix://var/run/docker.sock',  # or tcp://127.0.0.1:xxxx
    },
    {
        'name': 'HOST_B',
        'hostname': 'localhost',
        'socket': 'http+unix://var/run/docker.sock',
    }
]

APPS = [
    {
        'name': 'WORDPRESS_4.3',
        'image': 'wordpress:4.3-apache',
        # TODO: methode de deploiement / callback
    },
    {
        'name': 'MYSQL_5.7',
        'image': 'mysql:5.7',
        # TODO: methode de deploiement / callback
    },
    {
        'name': 'DEBIAN_JESSIE',
        'image': 'debian:jessie',
        'command': 'sleep 5'
    }
]

wordpress_deployment_config = {
    'HOSTS': HOSTS,
    'APPS': APPS,
}
