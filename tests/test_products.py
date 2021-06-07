from falcon import testing
import pytest

from app import app


@pytest.fixture
def client():
    return testing.TestClient(app)


def test_list_products(client):
    response = client.simulate_get('/products')
    assert response.status_code == 404
