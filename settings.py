import time
import base64
import subprocess
import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=['.env.app','.env.postgres','.env.redis'], env_file_encoding='utf-8',extra='allow')

    
config = Settings().model_dump()    
# VARIABLES
PRODUCTION_BUILD = config['production_build']
PG_HOST = config['postgres_production_url'] if config['production_build'] == 'True' else config['postgres_development_url']
 # While docker - compose build this takes url as cont name
PG_PASS = config['postgres_password']
PG_USER = config['postgres_user']
PG_DB_NAME = config['postgres_db']
PG_PORT=config['postgres_port']
DOCKER_RUN = config['docker_run_pg'] if config['production_build'] == 'False' else config['hello']
    # N O T I C E   ---    While building app dev mode this part running "docker run postgres container" outside app
result = subprocess.run(str(config['docker_run_pg']), shell=True, \
                            stdout=subprocess.PIPE, encoding='utf-8')           
print(result.stdout)
time.sleep(10)

CONTACT_NAME = config['contact_name']
CONTACT_EMAIL = config['contact_email']
API_DESCRIPTION = config['api_description']
API_TITLE = config['api_title']
# jwt things
JWT_TOKEN_LIFETIME = config['jwt_token_lifetime']
# REDIS cache
CACHE_EXP = config['cache_exp']
REDIS_URL = config['prod_redis_url'] if config['production_build'] == 'True' else config['dev_redis_url']
CACHE_PREFIX = config['cache_prefix']

# JWT
JWT_SECRET_KEY = config['jwt_secret_key']
JWT_ALGORITHM = config['jwt_algorithm']
JWT_TOKEN_LIFETIME = config['jwt_token_lifetime']  

#Since the beginning that was bytes but i cut b then made it bytes
HASH_CRYPTO_KEY = bytes(config['hash_crypto_key'],'utf-8')
# uvicorn src.app:app --reload
RESET_PASSWORD_SECRET_KEY = bytes(config['reset_password_secret_key'],'utf-8')
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