import yaml
import os
from dataclasses import dataclass


def load_config_file(env_name: str):
    with open(f'config/{env_name}.yaml') as f:
        return yaml.safe_load(f)


@dataclass
class BaseConfig:
    APP_NAME: str
    LOG_LEVEL: str

    CELERY_BROKER_URL: list

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    DB_PG_NAME: str
    DB_SCHEMA: str
    DB_PG_USERNAME: str
    DB_PG_PASSWORD: str
    DB_PG_HOST: str
    DB_PG_PORT: int = 5432

    @property
    def DB_PG_URL(self):
        return 'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(
            user=self.DB_PG_USERNAME,
            password=self.DB_PG_PASSWORD,
            host=self.DB_PG_HOST,
            port=self.DB_PG_PORT,
            db_name=self.DB_PG_NAME,
        )




class DevConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    pass


def get_environment_name():
    return os.environ.get('ENVIRONMENT').lower() or 'dev'


def get_config():
    env_name = get_environment_name()
    source_data_config = load_config_file(env_name)
    return {
        'dev': DevConfig,
        'test': TestConfig,
        'prod': ProdConfig
    }[env_name](**source_data_config)


config = get_config()
