import os
import requests
from datetime import datetime
import logging

from db import model as m
from tasks.celery import app


@app.task
def call_ms():
    """Calls offers ms, update/create offers and insert price change
    into offer_prices table."""
    url = os.environ.get('OFFERS_URL')

    headers = {
        'Bearer': os.environ.get('AUTH_TOKEN')
    }

    products = m.Product.select()

    if not products:
        logging.info('No products!')
        return

    for product in products:
        logging.info(product.id)
        resp = requests.get(
            url + '/products/' + product.id + '/offers',
            headers=headers
        )
        if resp.status_code != 200:
            logging.info(f'Failed call for product: {product.id}')
            continue

        logging.info(resp)

        logging.info(f'Offers for product {product.id} updated!')
