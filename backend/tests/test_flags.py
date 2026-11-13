from app.db.models import FeatureFlag, Rule
from app.db.session import get_db
from app.api.constant import FLAGS
from app.main import app
from fastapi.testclient import TestClient
import pytest, constant as con

@pytest.fixture()
def config():
    """Provide a TestClient and the flag endpoint path for tests."""
    client=TestClient(app)
    endpoint = "/" + FLAGS
    return client, endpoint

#CREATE FLAG

def test_create_flag_success(db_session, config):
    """Verify creating a flag with valid payload returns 201."""
    try:
        client , endpoint = config
        endpoint+="/"
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
        endpoint+="/"
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
        endpoint+="/"
        app.dependency_overrides[get_db] = lambda: db_session  # fixture session
        request_one = con.TEST_FLAG_PYDANTIC_FAIL_ONE
        request_two = con.TEST_FLAG_PYDANTIC_FAIL_TWO
        response_one = client.post(endpoint, json=request_one)
        response_two = client.post(endpoint, json=request_two)
        assert response_one.status_code == 422 and response_two.status_code == 422
    finally:
        app.dependency_overrides.clear()

# GET FLAG

def test_get_flag_success(db_session, config):
    """Verify given rules and feature flag and return 200."""
    try:
        client, endpoint = config
        flag_key=con.TEST_GET_FLAG_KEY
        endpoint+="/" + flag_key
        app.dependency_overrides[get_db] = lambda: db_session # fixture session per test

        fake_db_flag=FeatureFlag(flag_key=flag_key, enabled=True, rollout_percentage=con.TEST_ROLLOUT_Q, description=con.TEST_FLAG_DESC, target_users=con.TEST_FLAG_TARGET_U)
        db_session.add(fake_db_flag)
        db_session.flush()

        fake_db_rule=Rule(feature_flag_id=fake_db_flag.id, name=con.TEST_RULE_NAME, conditions=con.TEST_RULE_COND, enabled=con.TEST_RULE_ENABLED, rule_type=con.TEST_RULE_TYPE)
        db_session.add(fake_db_rule)
        db_session.commit()

        response=client.get(endpoint)
        data=response.json()
        rules=data["rules"][0]
        assert data["id"]==fake_db_flag.id
        assert data["enabled"]==True
        assert data["flag_key"]==con.TEST_GET_FLAG_KEY
        assert data["rollout_percentage"]==con.TEST_ROLLOUT_Q
        assert data["target_users"]==con.TEST_FLAG_TARGET_U
        assert data["description"]==con.TEST_FLAG_DESC
        assert rules["enabled"]==con.TEST_RULE_ENABLED
        assert rules["name"]==con.TEST_RULE_NAME
        assert rules["conditions"]==con.TEST_RULE_COND
        assert rules["rule_type"]==con.TEST_RULE_TYPE
        assert response.status_code==200
    finally:
        app.dependency_overrides.clear()

def test_get_flag_no_rule_success(db_session, config):
    """Verify given empty rules and feature flag and return 200."""
    try:
        client, endpoint = config
        flag_key=con.TEST_GET_FLAG_KEY
        endpoint+="/" + flag_key
        app.dependency_overrides[get_db] = lambda: db_session # fixture session per test

        fake_db_flag=FeatureFlag(flag_key=flag_key, enabled=True, rollout_percentage=con.TEST_ROLLOUT_Q, description=con.TEST_FLAG_DESC, target_users=con.TEST_FLAG_TARGET_U)
        db_session.add(fake_db_flag)
        db_session.commit()

        response=client.get(endpoint)
        data=response.json()
        rules=data["rules"]
        assert rules==[]
        assert response.status_code==200
    finally:
        app.dependency_overrides.clear()

def test_get_flag_failure(db_session, config):
    """Verify failure with non-existing feature flag in DB, return 404."""
    try:
        client, endpoint = config
        flag_key=con.TEST_GET_FLAG_KEY
        endpoint+="/" + flag_key
        app.dependency_overrides[get_db] = lambda: db_session # fixture session per test

        response=client.get(endpoint)
        assert response.status_code==404
    finally:
        app.dependency_overrides.clear()
