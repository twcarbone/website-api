import os

import dotenv
import sqlalchemy

dotenv.load_dotenv(".env")


class Config:
    # Misc configs
    DB_DRIVER = "postgresql+psycopg2"
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_ADMIN = os.getenv("DB_ADMIN")
    DB_USER_PW = os.getenv("DB_USER_PW")
    DB_ADMIN_PW = os.getenv("DB_ADMIN_PW")

    # Flask configs
    SECRET_KEY = os.getenv("SECRET_KEY")

    @classmethod
    @property
    def SQLALCHEMY_DATABASE_URI(cls):
        return sqlalchemy.URL.create(
            drivername=cls.DB_DRIVER,
            # TODO: Connect to database as super user ok?
            username=cls.DB_ADMIN,
            password=cls.DB_ADMIN_PW,
            host=cls.DB_HOST,
            port=cls.DB_PORT,
            database=cls.DB_NAME,
        )


class DevConfig(Config):
    DB_NAME = "web_dev"


class TestConfig(Config):
    TESTING = True
    DB_NAME = "web_test"


class ProdConfig(Config):
    DB_NAME = "web_prod"
