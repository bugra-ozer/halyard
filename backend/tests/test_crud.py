from app.db.crud import create_flag, get_flag_by_key, get_flags, delete_flag
from app.schemas.flags import FlagCreate
from tests import constant as con

def make_flag(session, flag_key=con.TEST_FLAG_KEY, enabled=True):
    flag_data = FlagCreate(flag_key=flag_key, enabled=enabled)
    created_flag = create_flag(session, flag_data)
    return created_flag

def test_create_flag(session):
    """Verify creating a flag with valid data returns it."""
    flag_data = FlagCreate(flag_key=con.TEST_FLAG_KEY, enabled = True)
    created_flag = create_flag(session, flag_data)

    assert created_flag.id is not None
    assert created_flag.flag_key == flag_data.flag_key
    assert created_flag.enabled == flag_data.enabled

def test_get_flag_by_key(session):
    """Verify getting a flag with valid data returns it."""
    created_flag = make_flag(session)

    retrieved_flag = get_flag_by_key(session, created_flag.flag_key)

    assert retrieved_flag is not None
    assert retrieved_flag.id == created_flag.id
    assert retrieved_flag.flag_key == created_flag.flag_key
    assert retrieved_flag.enabled == created_flag.enabled

def test_get_flags(session):
    """Verify getting all flags with valid data returns it."""
    created_flag = make_flag(session)

    retrieved_flags = get_flags(session)

    assert len(retrieved_flags) == 1
    assert retrieved_flags[0].id == created_flag.id
    assert retrieved_flags[0].flag_key == created_flag.flag_key
    assert retrieved_flags[0].enabled == created_flag.enabled

def test_delete_flag(session):
    """Verify deleting a flag with valid data removes it."""
    created_flag = make_flag(session)

    delete_flag(session, created_flag.flag_key)
    retrieved_flag = get_flag_by_key(session, created_flag.flag_key)

    assert retrieved_flag is None
    

