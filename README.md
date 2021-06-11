# product-aggregator

## Task

Create REST API JSON Python microservice, which allows to browse a product catalog and automatically updates prices from the offer service.

## Start the app

Application can be started via docker-compose: `docker-compose up`  
Before calling any endpoint, apply schema migration: `pem migrate`  
You need to start this command from db folder inside the web service container.  
Also the OFFERS_URL variable should be added into enfviles/web.env file

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

is:
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

