import falcon
import logging
import os
import requests

import falcon

class ProductsRessource:
import settings

    def on_post(self, req, resp):
        pass

    def on_get(self, req, resp, id):
        pass
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
        result = requests.get(
            settings.PRODUCT_REG_URL,
            headers=headers,
            json=payload
        )
        logging.info(result)
    def on_patch(self, req, resp, id):
        if not req.media:
            raise HTTPBadRequest

        Product.update(
            **req.media
        ).where(Product.id==id).execute()

    def on_delete(self, req, resp, id):
        result = Product.delete().where(
            Product.id==id
        ).execute()

        if not result:
            raise falcon.MediaNotFoundError("id")


class PriceTrendResource:

    def on_get(self, req, resp, id):
        logging.info("price trend GET!")


class PriceChangeResource:

    def on_get(self, req, resp, id):
        logging.info('price change GET!')


logging.basicConfig(level=logging.INFO)

app = falcon.App()

app.add_route('/v1/products', ProductResource())
app.add_route('/v1/products/{id:int}', ProductResource())
app.add_route('/v1/offer_prices/{id:int}/trend', PriceTrendResource())
app.add_route('/v1/offer_prices/{id:int}/percentage', PriceChangeResource())
