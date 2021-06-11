import os


OFFERS_URL = os.environ.get('OFFERS_URL')
PRODUCT_REG_URL = OFFERS_URL + '/products/register'

TOKEN_URL = os.environ.get('AUTH_TOKEN')
TOKEN = os.environ.get('TOKEN')

if TOKEN_URL:
    with open(TOKEN_URL, 'r') as file:
        TOKEN = file.read().splitlines()[0]

