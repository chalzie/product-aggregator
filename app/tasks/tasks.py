from datetime import datetime
import logging
import os
from peewee import IntegrityError
import requests

from db.model import Product, Offer, OfferPrice
from tasks.celery import app
import settings


@app.task
def call_ms():
    """Calls offers ms, update/create offers and insert price change
    into offer_prices table."""
    url = settings.OFFERS_URL
    headers = {'Bearer': settings.TOKEN}

    product_ids = [product.id for product in Product.select()]

    for id in product_ids:
        resp = requests.get(
            f'{url}/products/{str(id)}/offers',
            headers=headers
        )
        if resp.status_code != 200:
            logging.info(resp.status_code)
            logging.info(f'Failed offers MS request for product: {id}')
            continue

        for offer in resp.json():
            Offer.insert(
                id=offer['id'],
                price=offer['price'],
                items_in_stock=offer['items_in_stock'],
                product_id=id
            ).on_conflict(
                conflict_target=[Offer.id],
                update={Offer.price: offer['price'],
                        Offer.items_in_stock: offer['items_in_stock']}
            ).execute()

            OfferPrice.insert(
                offer_id=offer['id'],
                price=offer['price'],
                dtc=datetime.now()
            ).execute()

        logging.info(f'Offers for product {id} updated!')
