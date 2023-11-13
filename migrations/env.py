import logging
import re
from logging.config import fileConfig

import sqlalchemy as sa
from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from api import db

from config import Config

USE_TWOPHASE = False


# this is the Alembic Config object, which provides access to the values within the .ini
# file in use.
config = context.config


# Interpret the config file for Python logging. This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


# If a db section is passed using the '-x' option, only target that database for the
# migration. Otherwise, target all databases.
cmd_kwargs = context.get_x_argument(as_dictionary=True)
if cmd_kwargs:
    db_names = [cmd_kwargs["db"]]
else:
    db_names = re.split(r",\s*", config.get_main_option("databases"))


import api.models

target_metadata = {
    "dev": db.metadata,
    "test": db.metadata,
    "prod": db.metadata,
}


def run_migrations_offline() -> None:
    pass  # Not used


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # for the direct-to-DB use case, start a transaction on all
    # engines, then run all migrations, then commit all transactions.

    engines = {}
    for name in db_names:
        engines[name] = rec = {}
        rec["engine"] = api.models.engine(
            user=Config.DB_ADMIN,
            password=Config.DB_ADMIN_PW,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=f"web_{name}",
        )

    for name, rec in engines.items():
        engine = rec["engine"]
        rec["connection"] = conn = engine.connect()

        if USE_TWOPHASE:
            rec["transaction"] = conn.begin_twophase()
        else:
            rec["transaction"] = conn.begin()

    try:
        for name, rec in engines.items():
            logger.info("Migrating database %s" % name)
            context.configure(
                connection=rec["connection"],
                upgrade_token="%s_upgrades" % name,
                downgrade_token="%s_downgrades" % name,
                target_metadata=target_metadata.get(name),
            )
            context.run_migrations(engine_name=name)

        if USE_TWOPHASE:
            for rec in engines.values():
                rec["transaction"].prepare()

        for rec in engines.values():
            rec["transaction"].commit()
    except:
        for rec in engines.values():
            rec["transaction"].rollback()
        raise
    finally:
        for rec in engines.values():
            rec["connection"].close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
