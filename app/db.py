"""
Peewee is an SQLite ORM
"""
import os
from peewee import *
import datetime

db = SqliteDatabase((os.environ.get('APP_DATA') or '/usr/app-data')
                    + '/history.db')


class BaseModel(Model):
    class Meta:
        database = db


class History(BaseModel):
    name = CharField(null=True)
    phone = CharField(null=True)
    phone_date = DateTimeField(default=datetime.datetime.now)
