from collections.abc import Generator
from sqlalchemy import Connection, Engine, create_engine
from sqlalchemy.orm import Session
from app.db.session import DATABASE_URL_LOCAL
import pytest

@pytest.fixture(scope="session")
def test_engine()->Engine:
    """Prepares an engine per test suite, without a live session via given DATABASE_URL."""
    return create_engine(DATABASE_URL_LOCAL)

@pytest.fixture(scope="function")
def db_connection(test_engine: Engine)->Generator[Connection, None, None]:
    """Creates live connection on the fly per test starting from clean state and closes it automatically."""
    with test_engine.connect() as con:
        yield con

@pytest.fixture(scope="function")
def db_session(db_connection:Connection)->Generator[Session, None, None]:
    """Interrupts all transactions and rolls back DB to default state."""
    transaction = db_connection.begin()
    session = Session(bind=db_connection)
    try:yield session
    finally:
        session.close()
        transaction.rollback()