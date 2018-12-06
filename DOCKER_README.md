# Docker instructions

While on the root directory of the repo build the Docker image with the following command:
```
$ docker build -t grnet/travel .
```

Run the following commands to create the container and bring it up:
```
$ docker create --name travel-dev -it -v `pwd`:/srv/travel -v /srv/travel/travelsFront/dist -v /srv/travel/travelsFront/tmp -v /srv/travel/travelsFront/node_modules -v /srv/travel/travelsFront/bower_components -p 127.0.0.1:8080:8000 grnet/travel
$ docker start travel-dev
```

Travel can be accessed at localhost:8080.
To check the output of ember builder and manage.py runserver, run `docker logs [-f] travel-dev`

The database will be created in ./travelsBackend (mydb-docker.sqlite3) and it will be reused across docker builds. If you want to reset it, just remove the file. If you want to use an existing database, overwrite it. You'll probably need root, as Docker runs and therefore creates/modifies files as root.

If you want to access the container directly you can use the following command
```
$ docker exec -it travel-dev bash
```

# Troubleshooting:
- If you get the error "docker: Error response from daemon: Conflict" you have to remove previously created containers before creating a new one. Use `docker rm -f travel-dev`.
