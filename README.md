# Cursus

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Frichardnguyen99%2Fcursus%2Fmain%2Fpyproject.toml)](https://github.com/richardnguyen99/cursus/blob/main/pyproject.toml) [![GitHub release (with filter)](https://img.shields.io/github/v/release/richardnguyen99/cursus?logo=github)](https://github.com/richardnguyen99/cursus/releases/tag/0.0.1) [![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/richardn1999/cursus/latest?logo=docker&labelColor=rgba(229%2C242%2C252%2C1)&color=rgba(29%2C99%2C237%2C1))](https://hub.docker.com/repository/docker/richardn1999/cursus/general)

An open-source API repository for public universities.

## Disclaimer

This API is not affilitated with any universities. The data is collected based
on public search engines with public information. Information may be incorrect,
unofficial, or outdated. Please use with caution.

The data is a collection of information from universities' public information.
If you couldn't find the information you need, or the information is incorrect,
please send an email to [richard@richardhnguyen.com](richard@richardhnguyen.com)
for your request.

## Working directory

```sh
.
├── cursus              # Core directory
│   ├── app.py          # Main Flask application
│   ├── config.py       # Configuration file
│   ├── __init__.py   
│   ├── apis/           # API endpoints
│   ├── models/         # ORM models for database         
│   ├── schema/         # Pydantic schemas-to-json for APIs
│   ├── static/         # Static files
│   ├── templates/      # HTML pages
│   ├── util/           # Utility functions
│   └── views/          # Flask views and blueprints
├── data/               # Initial data for development
├── migrations/         # Alembic migration folder
├── nginx/              # Nginx configuration (development)
├── sql/                # Backup SQL scripts
├── test/               # Test directory
├── docker-compose.yml  # Docker compose to orchestrate docker containers
├── Dockerfile          # Python Docker image for development
├── Dockerfile.prod     # Python Docker image for production
├── manage.py           # CLI script
└── pyproject.toml      # Core Python configuration
```

## Installation

### Pre-requisites

- Python ([`python>=3.11`](https://www.python.org/downloads/release/python-3115/))
- Git ([https://git-scm.com/downloads](https://git-scm.com/downloads))
- Docker ([https://docs.docker.com/desktop](https://docs.docker.com/desktop))
- Virtualenv ([https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html))

### Clone the repository

```sh
git clone https://github.com/richardnguyen99/cursus.git
```

### Create an `.env` file

You need to create an `.env` file in order to start the application. The `.env`
will be used by Docker Compose to set up and boot up all the docker containers.
For example,

```sh
APP_SETTINGS="cursus.config.DevConfig"


POSTGRES_USER="postgres"
POSTGRES_PASSWORD="something-secret"
POSTGRES_DB="cursus"
PGPORT=7432
DATABASE_URL="postgresql://postgres:something-secret@172.26.0.2:7432/cursus"

PGADMIN_DEFAULT_EMAIL="richard@richardhnguyen.com"
PGADMIN_DEFAULT_PASSWORD="pgadmin"
PGADMIN_LISTEN_PORT=5050
```

Please check [`.env.example`](https://github.com/richardnguyen99/cursus/blob/main/.env.example) for more details.

> `DATABASE_URL` might be different depending on your docker network. You can
> check the IP Addres for the `postgres` container by running `docker inspect
> <container_id> | grep IPAddress`.

### Run with docker-compose

```sh
docker-compose up --build
```

Docker Compose will boot up everything for you. You can access the application
with these following URLs:

- `http://locahost`: The main application. NGINX will serve as the reverse proxy
  for the application. Every request will be redirected to the application.
- `http://localhost:5050`: The Flask application.
- `http://admin.localhost`: The PGAdmin application.
- `http://localhost:7432`: The PostgreSQL database.

### Run first migration

First, you need to install `alembic` to run the migration. I recommend you to
install it in a virtual environment with your choice of package manager. After
activating the virtual environment, run:

```sh
python3 manage.py db upgrade
```

This will run the first migration to create the database schema for you.

## LICENSE

This project is licensed under the terms of the MIT license.
