from dotenv import dotenv_values
import pathlib
import os
import time
import base64
import subprocess

# ROOT DIRECTORY OF THE PROJECT
root_dir = pathlib.Path(__file__).parent.resolve()

# DOTENV FILE
config = dotenv_values(f"{root_dir}/.env")
PRODUCTION_BUILD = config['PRODUCTION_BUILD']
PG_HOST = config['POSTGRES_PRODUCTION_URL'] if config['PRODUCTION_BUILD'] == 'True' else config['POSTGRES_DEVELOPMENT_URL']
 # While docker - compose build this takes url as cont name
PG_PASS = config['POSTGRES_PASSWORD']
PG_USER = config['POSTGRES_USER']
PG_DB_NAME = config['POSTGRES_DB']
PG_PORT=config['POSTGRES_PORT']
DOCKER_RUN = config['DOCKER_RUN_PG'] if config['PRODUCTION_BUILD'] == 'False' else config['HELLO']
    # N O T I C E   ---    While building app dev mode this part running "docker run postgres container" outside app
result = subprocess.run(str(config['DOCKER_RUN_PG']), shell=True, \
                            stdout=subprocess.PIPE, encoding='utf-8')           
print(result.stdout)
time.sleep(10)
JWT_TOKEN_LIFETIME = config['JWT_TOKEN_LIFETIME']
# REDIS cache
CACHE_EXP = config['CACHE_EXP']
REDIS_URL = config['PROD_REDIS_URL'] if config['PRODUCTION_BUILD'] == 'True' else config['DEV_REDIS_URL']
CACHE_PREFIX = config['CACHE_PREFIX']

# JWT
JWT_SECRET_KEY = config['JWT_SECRET_KEY']
JWT_ALGORITHM = config['JWT_ALGORITHM']
JWT_TOKEN_LIFETIME = config['JWT_TOKEN_LIFETIME']  

#Since the beginning that was bytes but i cut b then made it bytes
HASH_CRYPTO_KEY = bytes(config['HASH_CRYPTO_KEY'],'utf-8')
# uvicorn src.app:app --reload
RESET_PASSWORD_SECRET_KEY = bytes(config['RESET_PASSWORD_SECRET_KEY'],'utf-8')
# OPEN API TAGS

tags_meta = [
    {
        "name": "Users",
        "description": "***User Management Authentication[UMA]*** methods flow. Registration, Authentication, Reset password, typical UMA user flow.",
        "externalDocs": {
            "description": "Any question?",
            "url": "https://t.me/ewanG808",
        
        },

    },
    {
        "name": "Company",
        "description": "***Company*** ORM model and it's methods for making CRUD operations. Company - represents company item with data fields.",
        "externalDocs": {
            "description": "Any question?",
            "url": "https://t.me/ewanG808",
        
        },

    },
    {
        "name": "Employee",
        "description": "***Employee*** Methods for ORM model that extends User model. Employee - gives additional data structure to user that became as employee. Logically user may change the employment position so someone may substitute **user** on particular position. When particular _user_ is unemployed he has no Employee table...\nThis table extends user which works in the company on a position.",
        "externalDocs": {
            "description": "Any question?",
            "url": "https://t.me/ewanG808",
        
        },
    },
]