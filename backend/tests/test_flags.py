from app.db.models import FeatureFlag, Rule
from app.db.session import get_db
from app.api.constant import EP_FLAGS
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import select
import pytest, constant as con


@pytest.fixture()
def config():
    """Provide a TestClient and the flag endpoint path for tests."""
    client=TestClient(app)
    endpoint = "/" + EP_FLAGS
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
        rules=data[con.KEY_RULES][0]
        assert data[con.KEY_ID]==fake_db_flag.id
        assert data[con.KEY_ENABLED]==True
        assert data[con.KEY_FLAG_KEY]==con.TEST_GET_FLAG_KEY
        assert data[con.KEY_ROLLOUT_PERCENTAGE]==con.TEST_ROLLOUT_Q
        assert data[con.KEY_TARGET_USERS]==con.TEST_FLAG_TARGET_U
        assert data[con.KEY_DESCRIPTION]==con.TEST_FLAG_DESC
        assert rules[con.KEY_ENABLED]==con.TEST_RULE_ENABLED
        assert rules[con.KEY_NAME]==con.TEST_RULE_NAME
        assert rules[con.KEY_CONDITIONS]==con.TEST_RULE_COND
        assert rules[con.KEY_RULE_TYPE]==con.TEST_RULE_TYPE
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
        rules=data[con.KEY_RULES]
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

# GET FLAGS

def test_get_flags_success(db_session, config):
    """Verify the server returns flags are same as in populated DB, no rules and status code 200."""
    try:
        client, endpoint = config
        flag_key_one=con.TEST_GET_FLAG_KEY
        flag_key_two=con.TEST_FLAG_KEY
        endpoint += "/"
        app.dependency_overrides[get_db] = lambda: db_session  # fixture session per test

        fake_db_flag_one=FeatureFlag(flag_key=flag_key_one, enabled=True, rollout_percentage=con.TEST_ROLLOUT_Q, description=con.TEST_FLAG_DESC, target_users=con.TEST_FLAG_TARGET_U)
        fake_db_flag_two=FeatureFlag(flag_key=flag_key_two, enabled=True, rollout_percentage=con.TEST_ROLLOUT_Q, description=con.TEST_FLAG_DESC, target_users=con.TEST_FLAG_TARGET_U)
        db_session.add(fake_db_flag_one)
        db_session.add(fake_db_flag_two)
        db_session.commit()

        response = client.get(endpoint)
        data = response.json()
        assert response.status_code == 200
        assert len(data)==2
        assert flag_key_one in data[0][con.KEY_FLAG_KEY] and flag_key_two in data[1][con.KEY_FLAG_KEY]
    finally:
        app.dependency_overrides.clear()

def test_get_flags_failure(db_session, config):
    """Verify the server returning no flags and no rules in non-populated DB, and status code 200."""
    try:
        client, endpoint = config
        endpoint += "/"
        app.dependency_overrides[get_db] = lambda: db_session  # fixture session per test

        response = client.get(endpoint)
        data = response.json()
        assert len(data)==0
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()

# PATCH FLAG

def test_patch_flag_success(db_session, config):
    """Verify the server patching given existing flag and returns status code 200."""
    try:
        client, endpoint = config
        flag_key=con.TEST_GET_FLAG_KEY
        endpoint += "/" + flag_key
        app.dependency_overrides[get_db] = lambda: db_session  # fixture session per test

        fake_db_flag=FeatureFlag(flag_key=flag_key, enabled=True, rollout_percentage=con.TEST_ROLLOUT_Q, description=con.TEST_FLAG_DESC, target_users=con.TEST_FLAG_TARGET_U)
        db_session.add(fake_db_flag)
        db_session.commit()

        patch_json={con.KEY_ROLLOUT_PERCENTAGE: con.TEST_ROLLOUT_Q2}

        response = client.patch(endpoint, json=patch_json)
        data = response.json()
        assert data[con.KEY_ROLLOUT_PERCENTAGE]==con.TEST_ROLLOUT_Q2
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()

def test_patch_flag_failure(db_session, config):
    """Verify the server gracefully returns status code 404."""
    try:
        client, endpoint = config
        flag_key=con.TEST_GET_FLAG_KEY
        endpoint += "/" + flag_key
        app.dependency_overrides[get_db] = lambda: db_session  # fixture session per test

        patch_json={con.KEY_ROLLOUT_PERCENTAGE: con.TEST_ROLLOUT_Q2}

        response = client.patch(endpoint, json=patch_json)
        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()

def test_patch_flag_false_type(db_session, config):
    """Verify the server false data type patching attempt falls into Pydantic status code 422."""
    try:
        client, endpoint = config
        flag_key=con.TEST_GET_FLAG_KEY
        endpoint += "/" + flag_key
        app.dependency_overrides[get_db] = lambda: db_session  # fixture session per test

        fake_db_flag=FeatureFlag(flag_key=flag_key, enabled=True, rollout_percentage=con.TEST_ROLLOUT_Q, description=con.TEST_FLAG_DESC, target_users=con.TEST_FLAG_TARGET_U)
        db_session.add(fake_db_flag)
        db_session.commit()

        patch_one={con.KEY_ROLLOUT_PERCENTAGE: con.TEST_FLAG_DESC}
        patch_two={con.TEST_FLAG_KEY: con.TEST_RULE_NAME}

        response_one = client.patch(endpoint, json=patch_one)
        response_two = client.patch(endpoint, json=patch_two)
        assert response_one.status_code == 422
        assert response_two.status_code == 422
    finally:
        app.dependency_overrides.clear()

# DELETE FLAG

def test_delete_flag_success(db_session, config):
    """Verify deleting a flag and return 204."""
    try:
        client, endpoint = config
        flag_key=con.TEST_GET_FLAG_KEY
        endpoint+="/" + flag_key
        app.dependency_overrides[get_db] = lambda: db_session # fixture session per test

        fake_db_flag=FeatureFlag(flag_key=flag_key, enabled=True, rollout_percentage=con.TEST_ROLLOUT_Q, description=con.TEST_FLAG_DESC, target_users=con.TEST_FLAG_TARGET_U)
        db_session.add(fake_db_flag)
        db_session.commit()

        response=client.delete(endpoint)
        stmt = select(FeatureFlag).where(FeatureFlag.flag_key == flag_key)
        feature_flag = db_session.scalar(stmt)
        assert feature_flag is None
        assert response.status_code==204
    finally:
        app.dependency_overrides.clear()

def test_delete_flag_failure(db_session,  config):
    """Verify deleting a non-existing flag returns 404."""
    try:
        client, endpoint = config
        flag_key=con.TEST_GET_FLAG_KEY
        endpoint+="/" + flag_key
        app.dependency_overrides[get_db] = lambda: db_session # fixture session per test

        response=client.delete(endpoint)
        stmt = select(FeatureFlag).where(FeatureFlag.flag_key == flag_key)
        feature_flag = db_session.scalar(stmt)
        assert feature_flag is None
        assert response.status_code==404
    finally:
        app.dependency_overrides.clear()