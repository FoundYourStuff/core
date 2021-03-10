# Found Your Stuff Core

This is the repository for the backend API for the Found Your Stuff (FYS) item tracking system. 

## Status

This project is in active devleopment. We try to follow Git Flow and keep Master in a running state but no guarantees are made. **Running this in production is not recommended**. 

## Deployment

### Development 

The simplest way to run this application is with `docker-compose`. Please refer to the [offical instructions](https://docs.docker.com/compose/install/) to install `docker-compose`. 

**Install With docker-compose**
- clone this repository
- Run the docker containers with `docker-compose up -d`
  - The iniital run will pull images (if needed) and build the development image.
  - Ignore all warnings. **The `core_deployment` container will not start. This is a knonw bug**
- Check if the command succeeded with `docker ps`. You should see the following output
- Run the latest migration via alembic `docker-compose exec core_development /home/nonroot/.local/bin/alembic upgrade head`. This will execute alembic in the `core_development` docker container.
  - Look for the following output for success 
  ```
  INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
  INFO  [alembic.runtime.migration] Will assume transactional DDL.``` 
- Visit `localhost:8080/ui`. If everyting wokred, you should see the Swagger UI.  


