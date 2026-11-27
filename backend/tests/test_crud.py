from app.db.crud import create_flag
from app.schemas.flags import FlagCreate
from tests import constant as con

def test_create_flag(session):
    """Verify creating a flag with valid data returns it."""
    flag_data = FlagCreate(flag_key=con.TEST_FLAG_KEY, enabled = True)
    created_flag = create_flag(session, flag_data)

    assert created_flag.id is not None
    assert created_flag.flag_key == flag_data.flag_key
    assert created_flag.enabled == flag_data.enabled


