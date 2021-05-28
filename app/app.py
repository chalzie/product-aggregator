import falcon
import logging


class ProductsRessource:

    def on_post(self, req, resp):
        pass

    def on_get(self, req, resp, id):
        pass

    def on_put(self, req, resp, id):
        pass

    def on_delete(self, req, resp, id):
        pass


logging.basicConfig(level=logging.INFO)

app = falcon.App()
app.add_route('/products', ProductsResource())
app.add_route('/products/{id:int}', ProductsResource())
