# Docker instructions

You will need [docker-compose](https://docs.docker.com/compose/install/). 

While on the root directory of the repo use the following command:
```
# docker-compose up --build -d
```

This will create a container for the backend (manage.py runserver) and the frontend (ember build --watch). The containers are named `travel-backend` and `travel-frontend` respectively.

Travel can be accessed at localhost:8080.

To check the output of the container use docker logs, e.g. `docker logs [-f] travel-backend`

The database will be created in ./travelsBackend (mydb-docker.sqlite3) and it will be reused across docker builds. If you want to reset it, just remove the file. If you want to use an existing database, overwrite it. You'll probably need root, as Docker runs and therefore creates/modifies files as root.

If you want to run a shell in a container use
```
$ docker exec -it travel-backend bash
```

If you want to attach to the running process use:
```
$ docker attach travel-backend
```

## Running without docker-compose:
- To use the containers without docker-compose, you will have to build the containers, create and start them. You can check docker-compose.yml for info on options to use during container creation.
