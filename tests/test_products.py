from functools import wraps
from datetime import datetime

from falcon import testing
from playhouse.sqlite_ext import JSONField, SqliteExtDatabase
import pytest

from app import app
from db.model import db
from db.model import Product, Offer, OfferPrice


@pytest.fixture
def test_client():
    return testing.TestClient(app)


def with_test_db(dbs: tuple):
    def decorator(func):
        @wraps(func)
        def test_db_closure(*args, **kwargs):
            test_db = SqliteExtDatabase(":memory:")
            with test_db.bind_ctx(dbs):
                test_db.create_tables(dbs)
                try:
                    func(*args, **kwargs)
                finally:
                    test_db.drop_tables(dbs)
                    test_db.close()

        return test_db_closure

    return decorator


@with_test_db((Product,))
def test_get_products(test_client):
    Product.create(id=1, name="Tester", description="Test product")
    response = test_client.simulate_get('/v1/products/1')
    assert response.status_code == 200


@with_test_db((Product,))
def test_patch_product(test_client):
    Product.create(id=1, name="Tester", description="Test product")
    data = {
        "name": "Tester2"
    }
    response = test_client.simulate_patch('/v1/products/1', json=data)
    assert response.status_code == 200


@with_test_db((Product,))
def test_delete_product(test_client):
    Product.create(id=1, name="Tester", description="Test product")
    response = test_client.simulate_delete('/v1/products/1')
    assert response.status_code == 200


@with_test_db((Product, Offer, OfferPrice))
def test_prices_trend(test_client):
    Product.create(id=1, name="Tester", description="Test product")
    Offer.create(id=1, price=1, items_in_stock=10, product_id=1)
    OfferPrice.create(id=1, offer_id=1, price=2, dtc=datetime.now())
    OfferPrice.create(id=2, offer_id=1, price=3, dtc=datetime.now())
    OfferPrice.create(id=3, offer_id=1, price=4, dtc=datetime.now())
    response = test_client.simulate_get('/v1/offer_prices/1/trend?count=2')
    assert response.json['prices'] == [4, 3]
