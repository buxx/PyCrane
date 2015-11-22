
WORDPRESS_4_3_APACHE = 'wordpress:4.3-apache'  # my.registry.io:5000/wordpress:4.3
MYSQL_5_7 = 'mysql:5.7'

HOSTS_IMAGES = [
    WORDPRESS_4_3_APACHE,
    MYSQL_5_7
]

HOSTS = [
    {
        'name': 'HOST_A',
        'hostname': 'localhost',
        'socket': 'unix://var/run/docker.sock',
        'images': HOSTS_IMAGES
    },
    {
        'name': 'HOST_B',
        'hostname': 'localhost',
        'socket': 'unix://var/run/docker.sock',
        'images': HOSTS_IMAGES
    }
]

APPS = [
    {
        'name': 'WORDPRESS_4.3',
        'image': WORDPRESS_4_3_APACHE,
        # TODO: methode de deploiement / callback
    },
    {
        'name': 'MYSQL_5.7',
        'image': MYSQL_5_7,
        # TODO: methode de deploiement / callback
    }
]

wordpress_deployment_config = {
    'HOSTS': HOSTS,
    'APPS': APPS
}
