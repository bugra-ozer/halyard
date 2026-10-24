from fastapi.testclient import TestClient
from app.main import app
from app.constant import constant as con
import pytest

@pytest.fixture()
def config():
    client=TestClient(app)
    return client

def test_health_check(config):
        client=config
        response=client.get(con.HEALTH_ROUTE)
        assert response.status_code == 200