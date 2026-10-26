from app.services.evaluator import Evaluator
import pytest, constant as con

@pytest.fixture
def config():
    evaluator=Evaluator()
    return {con.KEY_FLAG_KEY: con.TEST_FLAG_KEY, con.KEY_EVALUATOR: evaluator, con.KEY_USER_ID: con.TEST_USER_ID, con.KEY_INC: con.TEST_TARGET_INC, con.KEY_EXC: con.TEST_TARGET_EXC}

def test_enabled_false(config):
    """Tests if class returns False while rest of the settings are set to be True."""
    config_dict=config
    evaluator, user_id, flag_key, targets=config_dict[con.KEY_EVALUATOR], config_dict[con.KEY_USER_ID], config_dict[con.KEY_FLAG_KEY], config_dict[con.KEY_INC]
    result=evaluator.evaluate(flag_key, False, con.TEST_FALLOUT_MAX, targets, user_id)
    assert result==False
    
def test_user_id_in_target_users(config):
    """"""
    config_dict=config
    evaluator, user_id, flag_key, targets=config_dict[con.KEY_EVALUATOR], config_dict[con.KEY_USER_ID], config_dict[con.KEY_FLAG_KEY], config_dict[con.KEY_INC]
    result=evaluator.evaluate(flag_key, True, con.TEST_FALLOUT_MIN, targets, user_id)
    assert result==True

def test_rollout_min(config):
    """"""
    config_dict=config
    evaluator, user_id, flag_key, targets=config_dict[con.KEY_EVALUATOR], config_dict[con.KEY_USER_ID], config_dict[con.KEY_FLAG_KEY], config_dict[con.KEY_EXC]
    result=evaluator.evaluate(flag_key, True, con.TEST_FALLOUT_MIN, targets, user_id)
    assert result==False

def test_rollout_max(config):
    """"""
    config_dict = config
    evaluator, user_id, flag_key, targets = config_dict[con.KEY_EVALUATOR], config_dict[con.KEY_USER_ID], config_dict[con.KEY_FLAG_KEY], config_dict[con.KEY_EXC]
    result = evaluator.evaluate(flag_key, True, con.TEST_FALLOUT_MAX, targets, user_id)
    assert result == True

def test_rollout_mid_empty_user(config):
    """"""
    config_dict = config
    evaluator, user_id, flag_key, targets = config_dict[con.KEY_EVALUATOR], con.TEST_USER_ID_EMPTY, config_dict[con.KEY_FLAG_KEY], config_dict[con.KEY_EXC]
    result_one = evaluator.evaluate(flag_key, True, con.TEST_FALLOUT_Q, targets, user_id)
    result_two = evaluator.evaluate(flag_key, True, con.TEST_FALLOUT_Q2, targets, user_id)
    assert result_one == False and result_two == False

def test_rollout_mid(config):
    """"""
    config_dict = config
    evaluator, user_id, flag_key, targets = config_dict[con.KEY_EVALUATOR], con.TEST_USER_ID, config_dict[con.KEY_FLAG_KEY], config_dict[con.KEY_EXC]
    result_one = evaluator.evaluate(flag_key, True, con.TEST_FALLOUT_Q, targets, user_id)
    result_two = evaluator.evaluate(flag_key, True, con.TEST_FALLOUT_Q2, targets, user_id)
    assert result_one == False and result_two == True