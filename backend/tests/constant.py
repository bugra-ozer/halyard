URL_TEST="http://test"
TEST_USER_STR= "robert"
TEST_USER_ID="xtpr"
TEST_USER_ID_EMPTY=""
TEST_TARGET_EXC={TEST_USER_STR}
TEST_TARGET_INC= {TEST_USER_STR, TEST_USER_ID}
TEST_FLAG_KEY= "feat_click"
TEST_ROLLOUT_Q=25
TEST_ROLLOUT_Q2=50
TEST_ROLLOUT_MAX=100
TEST_ROLLOUT_MIN=0


#Strings
KEY_EXC= "target_user_exc"
KEY_INC= "target_user_inc"
KEY_USER_ID= "user_id"
KEY_EVALUATOR= "evaluator"
KEY_FLAG_KEY="flag_key"


# Test flags

    # POST /flags
TEST_FLAG_SUCCESS=\
    {
  "flag_key": "beta_dashboard",
  "enabled": True,
  "rollout_percentage": 100
    }
TEST_FLAG_PYDANTIC_FAIL_ONE=\
    {
  "flag_key": "beta_dashboard",
  "enabled": True,
  "rollout_percentage": 200
    }
TEST_FLAG_PYDANTIC_FAIL_TWO=\
    {
  "enabled": True,
  "rollout_percentage": 100
    }

    #GET /flags/flag_key
TEST_GET_FLAG_KEY="products_dashboard"
TEST_FLAG_DESC="Dashboard that enables products to be discounted, removed, added, changed stocks."
TEST_FLAG_TARGET_U=['2','5','425']
TEST_RULE_NAME="UK_Beta"
TEST_RULE_TYPE="attribute_match"
TEST_RULE_COND={"user_country": "UK", "user_region": "England"}
TEST_RULE_ENABLED=True
