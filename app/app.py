from datetime import datetime
import logging
import os
import requests

import falcon
from peewee import fn

from db.model import Product, OfferPrice, Offer
import settings


class ProductListResource:

    def on_get(self, req, resp):
        resp.media = {
            'products': [],
        }
        try:
            products = Product.select().execute()
            logging.info(products)
        except:
            logging.info('error in products get list')

        if not products:
            raise falcon.HTTPNotFound

        for product in products:
            resp.media['products'].append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
            })
        resp.status = falcon.HTTP_200


class ProductResource:

    def on_post(self, req, resp):
        name = req.media.get('name', None)
        description = req.media.get('description', None)

        if not name:
            raise falcon.HTTPMissingParam(param_name="name")
        if not description:
            raise falcon.HTTPMissingParam(param_name="description")

        product_id = Product.insert(
            name=name, description=description
        ).execute()

        if not product_id:
            raise falcon.HTTPNotFound

        headers = {'Bearer': settings.TOKEN}
        payload = {
            "id": product_id,
            "name": name,
            "description": description
        }
        # result = requests.post(
        #     settings.PRODUCT_REG_URL,
        #     headers=headers,
        #     json=payload
        # )
        logging.info(result)

    def on_get(self, req, resp, id):
        try:
            product = Product.select(
                Product.id, Product.name, Product.description
            ).where(Product.id==id).get()
        except Product.DoesNotExist:
            raise falcon.HTTPNotFound

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': product.id,
            'name': product.name,
            'description': product.description
        }


    def on_patch(self, req, resp, id):
        if not req.media:
            raise falcon.HTTPBadRequest

        Product.update(
            **req.media
        ).where(Product.id==id).execute()

    def on_delete(self, req, resp, id):
        result = Product.delete().where(
            Product.id==id
        ).execute()

        if not result:
            raise falcon.MediaNotFoundError("id")


class OfferListResource:

    def on_get(self, req, resp, product_id):
        resp.media = {
            'offers': [],
        }

        offers = Offer.select().where(
            Offer.product_id==product_id
        ).execute()

        if not offers:
            raise falcon.HTTPNotFound

        for offer in offers:
            resp.media['offers'].append({
                'id': offer.id,
                'price': offer.price,
                'items_in_stock': offer.items_in_stock,
            })
        resp.status = falcon.HTTP_200


class PriceTrendResource:

    def on_get(self, req, resp, id):
        if 'count' not in req.params:
            raise falcon.HTTPMissingParam

        prices = []

        query = OfferPrice.select().where(
            OfferPrice.offer_id==id
        ).order_by(
            OfferPrice.dtc.desc()
        ).limit(req.params['count'])

        for price in query.execute():
            prices.append(price.price)
        logging.info(prices)

        resp.status = falcon.HTTP_200
        resp.media = {
            'prices': prices
        }


class PriceChangeResource:

    def on_get(self, req, resp, id):
        if 'from' not in req.params:
            raise falcon.HTTPMissingParam
        if 'to' not in req.params:
            raise falcon.HTTPMissingParam

        date_from = datetime.strptime(req.params['from'], '%d/%m/%y %H:%M:%S')
        date_to = datetime.strptime(req.params['to'], '%d/%m/%y %H:%M:%S')

        from_op = OfferPrice.select().where(
            (OfferPrice.dtc >= date_from) &
            (OfferPrice.offer_id==id)).order_by(
                OfferPrice.dtc).limit(1).get()

        to_op = OfferPrice.select().where(
            (OfferPrice.dtc <= date_to) &
            (OfferPrice.offer_id==id)).order_by(
                OfferPrice.dtc.desc()).limit(1).get()
        result = to_op.price / (from_op.price / 100) - 100
        logging.info(result)

        resp.status = falcon.HTTP_200
        resp.media = {
            'percentage': result
        }


logging.basicConfig(level=logging.INFO)

app = falcon.App()

app.add_route('/v1/products', ProductListResource())
app.add_route('/v1/products/{id:int}', ProductResource())
app.add_route('/v1/offers/{product_id:int}', OfferListResource())
app.add_route('/v1/offer_prices/{id:int}/trend', PriceTrendResource())
app.add_route('/v1/offer_prices/{id:int}/percentage', PriceChangeResource())
