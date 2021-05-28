import os

from peewee import Model, CharField, TextField, IntegerField
from peewee import PrimaryKeyField, ForeignKeyField

from playhouse.db_url import connect


class BaseModel(Model):
    class Meta:
        database  = connect(os.environ.get('PSQL'))


class Product(Model):
    id = PrimaryKeyField()
    name = TextField()
    description = TextField()


class Offers(Model):
    id = PrimaryKeyField()
    price = IntegerField()
    items_in_stock = IntegerField()
    product_id = ForeignKeyField(Product, backref="offers")
