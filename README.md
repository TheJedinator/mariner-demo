# What?

Example Application Using FastAPI SQLAlchemy and Alembic with PostgresQL for some simple user and permissions CRUD
operations

### Requirements specified:

A user should have at least the following attributes:

    family name
    given name
    birthdate
    email

A user's permission should have at least the following attributes:

    type
    granted date

The API should provide the endpoints to satisfy at least the following functional requirements:

    list users
    add user
    remove user
    get user by id
    grant permission for a user
    revoke permission for a user
    search users by family name

## Things I would do differently in production

- Way better and more error handling, logging
- Request more definition around some business logic required
- Security and IAM (secrets for database creds etc)
- Probably wouldn't use an ORM for performance and security reasons, prefer stored procs.

### Your obvious question: Then why didn't you here?

- I didn't want to re-invent any wheels or spend huge amounts of time getting things "perfect" for what amounts to a
  demo CRUD application

## Get Started

Pre-requisites: `python3.8, pip, psql, docker, docker-compose`
With this config you can't have a local postgresql instance running on 5432, or you can change the exposed port in
docker-compose.yml

Recommend new virtual environment, but that's your funeral.... Ensure nothing else is running locally on port 8000,
either kill it or change the port on line 129 of main.py

## Setup

1. cd into project directory: `pip3 install -r requirements`
2. `psql -h localhost -p 5432 -d postgres -U user` > `create database mariner`, `\q (to exit psql shell)`
3. In the main project directory execute: `alembic upgrade head` - to apply migrations to the database (sets up the
   schema)

## Run it

1. `docker-compose up`
2. cd into the src directory and run `python3 src/main.py`
3. The server is now running, you can view documentation and test the endpoints by navigating
   to `http://127.0.0.1:8000/docs`
