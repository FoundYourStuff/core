# Found Your Stuff Core

Backend API of the Found Your Stuff (FYS) project's item tracking system. 

## Status

This project is in active development. We try to follow [Git Flow](https://guides.github.com/introduction/flow/) and keep Master in a running state, but no guarantees are made. **Running this in production is not recommended**. 

## Deployment

### Development 

The simplest way to run this application is with `docker-compose`. Please refer to the [offical instructions](https://docs.docker.com/compose/install/) to install `docker-compose`. 

**Install With docker-compose**
- Clone this repository
- Run the docker containers with `docker-compose up -d`
  - The initial run will pull images (if needed) and build the development image.
  - Ignore all warnings. **The `core_deployment` container will not start. This is a known bug**
- Check if the command succeeded with `docker ps`. You should see the following output
  ``` 
  CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS             PORTS                      NAMES
  cd3033d0c549   core_core_development   "/sbin/tini -- nodem…"   33 minutes ago   Up 32 minutes      127.0.0.1:8080->8080/tcp   core_core_development_1
  5e55551a2a16   core_database           "docker-entrypoint.s…"   2 weeks ago      Up 32 minutes      5432/tcp                   core_database_
   ```
- Run the latest migration via alembic `docker-compose exec core_development /home/nonroot/.local/bin/alembic upgrade head`. This will execute alembic in the `core_development` docker container.
  - Look for the following output after running to determine if the run was a success 
  ```
  INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
  INFO  [alembic.runtime.migration] Will assume transactional DDL.``` 
- Visit `localhost:8080/ui`. If everything worked, you should see the Swagger UI.
