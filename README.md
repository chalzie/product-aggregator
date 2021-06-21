# product-aggregator

## Task

Create REST API JSON Python microservice, which allows to browse a product catalog and automatically updates prices from the offer service.

## Steps to reproduce development env

1. Add OFFERS_URL variable into envfiles/web.env file.
1. Build image and create container from the root folder with command: `docker-compose up --build`
1. Apply schema migration by executing to the `web` container: `docker-compose exec web bash`...
1. ... then move to the `db` folder and from there call the peewee-migration tool: `pem migrate`.
1. Now, as the database is initialized, you can call the endpoints defined in the `app.py` file:
   - `/v1/products` POST - to add new product and register it in the offers microservice
   - `/v1/products/<id>` GET, PATCH, DELETE - to get, update or delete specific product
   - `/v1/offers/<product_id>` GET - to get offers list for specific product
   - `/v1/offer_prices/<id>/trend` GET - to retrieve list of X last offer prices, X provided in params
   - `/v1/offer_prices/<id>/percentage` GET - to obtain rise/fall of the value between the dates in params

To run basic tests you can create virtual environment: `python -m venv venv` and `source venv/bin/activate`  
Then you need to install dependencies: `pip install -r requirements`  
The environment variables used in docker-compose and defined in envfiles folder must be created, e.g.:  
`export PYTHONPATH=app`  
`export OFFERS_URL=<offers_url>`  
`export TOKEN=<token>`

### Requirements

- Provide API to create, update and delete product
- Periodically query provided microservice for offers/shops with products

### Data model

Products - each product corresponds to a real world product you can buy  
id:  
name: string  
description: string

Offers - each offer represents a product offer being sold for some price somewhere  
id:  
price: integer  
items_in_stock: integer

#### Relations

- Product has many Offers
- Offer belongs to Product

### Specification

- use an SQL database as internal database
- request access token from the offers microservice (should be done only once, provide for all calls)
- create CRUD for products
- create background (job) service which periodically call the offers microservice to request new/updated offers for your products (price from offer ms is updated every minute).
- base URL for the Offers MS should be configurable via an environment variable
- write basic tests with pytest
- push your code into a public repo on Github
- add a README with information about how to start and use your service
