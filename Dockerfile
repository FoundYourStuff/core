# <--------------STAGE--------------> base
FROM python:alpine3.12 as base

RUN mkdir -p /var/app
WORKDIR /var/app

# Non-root user for security purposes.
RUN addgroup -g 10001 -S nonroot && adduser -u 10000 -S -G nonroot -h /home/nonroot nonroot

# Tini allows us to avoid several Docker edge cases, see https://github.com/krallin/tini.
# bind-tools is needed for DNS resolution to work in *some* Docker networks
# The rest is needed for sqlalchemy & related pg libs :|
RUN apk add --no-cache tini --no-cache bind-tools \
    postgresql-dev gcc python3-dev musl-dev

# Heroku CLI
RUN curl https://cli-assets.heroku.com/install.sh | sh

# Use the non-root user to run our application
USER nonroot

# <--------------STAGE--------------> deployment
FROM base as deployment

COPY . /var/app/

RUN export PATH="/home/nonroot/.local/bin:$PATH"
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/sbin/tini", "--", "python3"]

CMD ["api/__init__.py"]

# <--------------STAGE--------------> development
FROM base as development

COPY requirements.txt ./
COPY alembic.ini ./

EXPOSE 8080

RUN export PATH="/home/nonroot/.local/bin:$PATH"
RUN pip3 install -r requirements.txt

USER root
RUN apk add --update npm
RUN npm i -g nodemon
USER nonroot

ENTRYPOINT ["/sbin/tini", "--", "nodemon"]

CMD ["--exec", "python3", "api/__init__.py"]

# <--------------STAGE--------------> Blank Postgres
FROM postgres:12-alpine as database

ARG DB_USER=postgres
ARG DB_PASS=postgres
ARG DB_NAME=postgres

# Actually for pg
ENV POSTGRES_USER=${DB_USER}
ENV POSTGRES_PASSWORD=${DB_PASS}
ENV POSTGRES_DB=${DB_NAME}
