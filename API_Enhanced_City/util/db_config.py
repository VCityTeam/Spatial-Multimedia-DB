#!/usr/bin/env python3
# coding: utf8

from util.VarConfig import VarConfig
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
default_db_info = ('postgresql://''postgres:password'
                   '@localhost:5433/extendedDoc')


def get_db_info():
    config = VarConfig.get()
    return f'{config["SPATIAL_MULTIMEDIA_ORDBMS"]}://{config["SPATIAL_MULTIMEDIA_DB_USER"]}:' \
           f'{config["SPATIAL_MULTIMEDIA_DB_PASSWORD"]}@{config["SPATIAL_MULTIMEDIA_DB_HOST"]}:' \
           f'{config["SPATIAL_MULTIMEDIA_DB_PORT"]}/{config["SPATIAL_MULTIMEDIA_DB_NAME"]}'
