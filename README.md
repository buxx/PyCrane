# PyCrane

**PyCrane is in development mode, DO NOT USE IT FOR PRODUCTION YET**

A REST access point to control app deployment in docker containers

## Features

* List, create and manage application instances on defined hosts

## Features TO DO

* Accept instantiation callback to provide *volumes*, *port forwarding*, etc.

## In some words

Define yours hosts and apps in pythons dicts:

```
HOSTS = [
    {
        'name': 'HOST_A',
        'hostname': 'localhost',
        'socket': 'http+unix://var/run/docker.sock',  # or tcp://x.x.x.x:xxxx
    },
    # ...
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
    }
]

wordpress_deployment_config = {
    'HOSTS': HOSTS,
    'APPS': APPS,
}
```

At this point, no container is running on HOST_A:

```
➜  PyCrane git:(master) ✗ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

Create one with PyCrane:

```
➜  PyCrane git:(master) ✗ curl --data "name=WP_1&app=WORDPRESS_4.3&host=HOST_A&enabled=1" http://127.0.0.1:5000/instances
{
    "request": {
        "errors": []
    },
    "response": {
        "app": "WORDPRESS_4.3",
        "enabled": true,
        "host": "HOST_A",
        "image": "wordpress:4.3-apache",
        "name": "WP_1"
    }
}
```

Container corresponding to this app instance is running on HOST_A:
 
 ```
 ➜  PyCrane git:(master) ✗ docker ps
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS                                  PORTS               NAMES
43d36c7c2072        wordpress:4.3-apache   "/entrypoint.sh apach"   29 seconds ago      Restarting (1) Less than a second ago   80/tcp              wordpress_WP_1_1
```

To stop it:

```
➜  PyCrane git:(master) ✗ curl -X PUT -d "enabled=0" http://127.0.0.1:5000/instance/WP_1
{
    "request": {
        "errors": []
    },
    "response": {
        "app": "WORDPRESS_4.3",
        "enabled": "0",
        "host": "HOST_A",
        "image": "wordpress:4.3-apache",
        "name": "WP_1"
    }
}
```

No more container on HOST_A:

```
➜  PyCrane git:(master) ✗ docker ps                                                     
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```
