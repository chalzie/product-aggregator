import os

from peewee import Model, IntegerField
from peewee import DateTimeField, TextField
from peewee import AutoField, ForeignKeyField
from peewee import PostgresqlDatabase


db = PostgresqlDatabase(
    os.environ.get('POSTGRES_DATABASE'),
    user=os.environ.get('POSTGRES_USER'),
    password=os.environ.get('POSTGRES_PASSWORD'),
    host='db'
)


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    id = AutoField()
    name = TextField()
    description = TextField()

    class Meta:
        table_name = "products"


class Offer(BaseModel):
    id = AutoField()
    price = IntegerField()
    items_in_stock = IntegerField()
    product_id = ForeignKeyField(Product, backref="offers")

    class Meta:
        table_name = "offers"


class OfferPrice(BaseModel):
    id = AutoField()
    offer_id = ForeignKeyField(Offer, backref="prices")
    price = IntegerField()
    dtc = DateTimeField()

    class Meta:
        table_name = "offer_prices"
