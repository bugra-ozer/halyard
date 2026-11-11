from app.db.session import get_db
from app.api.constant import FLAGS
from app.main import app
from fastapi.testclient import TestClient
import pytest, constant as con

@pytest.fixture()
def config():
    """Provide a TestClient and the flag endpoint path for tests."""
    client=TestClient(app)
    endpoint="/" + FLAGS + "/"
    return client, endpoint

def test_create_flag_success(db_session, config):
    """Verify creating a flag with valid payload returns 201."""
    try:
        client, endpoint = config
        app.dependency_overrides[get_db] = lambda: db_session  # fixture session
        request = con.TEST_FLAG_SUCCESS
        response = client.post(endpoint, json=request)
        assert response.status_code == 201
    finally:
        app.dependency_overrides.clear()

def test_create_flag_duplicate(db_session, config):
    """Verify creating a duplicate flag returns 409."""
    try:
        client, endpoint = config
        app.dependency_overrides[get_db] = lambda: db_session  # fixture session
        request = con.TEST_FLAG_SUCCESS
        client.post(endpoint, json=request)
        response = client.post(endpoint, json=request)
        assert response.status_code == 409
    finally:
        app.dependency_overrides.clear()

def test_create_flag_pydantic_fail(db_session, config):
    """Verify Pydantic invalid requests return 422."""
    try:
        client, endpoint = config
        app.dependency_overrides[get_db] = lambda: db_session  # fixture session
        request_one = con.TEST_FLAG_PYDANTIC_FAIL_ONE
        request_two = con.TEST_FLAG_PYDANTIC_FAIL_TWO
        response_one = client.post(endpoint, json=request_one)
        response_two = client.post(endpoint, json=request_two)
        assert response_one.status_code == 422 and response_two.status_code == 422
    finally:
        app.dependency_overrides.clear()