# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Product(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    name = TextField()
    description = TextField()
    class Meta:
        table_name = "products"


@snapshot.append
class Offer(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    price = IntegerField()
    items_in_stock = IntegerField()
    product_id = snapshot.ForeignKeyField(backref='offers', index=True, model='product')
    class Meta:
        table_name = "offers"


@snapshot.append
class OfferPrice(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    offer_id = snapshot.ForeignKeyField(backref='history', index=True, model='offer')
    price = IntegerField()
    dtc = DateTimeField()
    class Meta:
        table_name = "offer_prices"


