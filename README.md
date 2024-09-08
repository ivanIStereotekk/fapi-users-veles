** Users management **

> [!NOTE]
> Приложение для - Auth User Management ( В процессе разработки ).


### Auth User App - Микросервис 

```.env
#    WHILE PRODUCTION TURN IT TRUE
PRODUCTION_BUILD=False
POSTGRES_PRODUCTION_URL=postgres_db
# url while run in local area
POSTGRES_DEVELOPMENT_URL=localhost
POSTGRES_PASSWORD=secret123
POSTGRES_USER=postgres

# Inner Postgres option: If it is not specified, then the value of POSTGRES_USER will be used.
POSTGRES_DB=xdb #database name look in the docker run command POSTGRES_DB
POSTGRES_PORT=5432
# This command  will run docker container while running app
#DOCKER_RUN_PG='docker run --name postgres --env=POSTGRES_USER=postgres_dev --env=POSTGRES_PASSWORD=secret123 --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/postgresql/16/bin --env=GOSU_VERSION=1.17 --env=LANG=en_US.utf8 --env=PG_MAJOR=16 --env=PG_VERSION=16.3-1.pgdg120+1 --env=PGDATA=/var/lib/postgresql/data --volume=/var/lib/postgresql/data -p 5432:5432 --restart=no --runtime=runc -t -d postgres:latest'
DOCKER_RUN_PG='docker run -it --name postgres_dev -e POSTGRES_DB=xdb -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=secret123 -p 5432:5432 -d postgres:latest'
JWT_TOKEN_LIFETIME=3600
CACHE_EXP=90
LOCAL_REDIS_URL='redis://localhost'
CACHE_PREFIX='veles-app'
CONTACT_NAME='Ivan Goncharov'
CONTACT_EMAIL='ivan.stereotekk@gmail.com'
API_TITLE='User Management Access - web application'
API_DESCRIPTION='VELES company user management REST methods'

HELLO='echo reading_envs_OK!'
# JWT Things
JWT_SECRET_KEY=e8cd77e6d45d7aa887a1a81d13512e135d9dbe9a62d16c3ee73bc51e2bb00c3f
JWT_TOKEN_LIFETIME=10080
JWT_ALGORITHM="HS256"
# Password hashing base64 -  Fernet.generate_key()
HASH_CRYPTO_KEY='aAGKiORWZxJc8vwnuE4xKmTkFNPK8k_UiYVkOBdWGoA='
RESET_PASSWORD_SECRET_KEY='7TZx6EmUG8k4HJ4c7p6NHhBZw-cs1PuEBBVyp28ENik='
# REDIS CACHE
DEV_REDIS_URL='redis://localhost'
PROD_REDIS_URL = 'redis://redis_cache'
CACHE_EXP=3600
CACHE_PREFIX='Veles-app:'
CONTACT_NAME='Ivan Goncharov'
CONTACT_EMAIL='ivan.stereotekk@gmail.com'
API_TITLE='VELES REST API  - [ web application ]'
API_DESCRIPTION='VELES REST endpoints or methods'




```

