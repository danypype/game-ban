from lib.db import Session

import pytest


@pytest.fixture(scope="session")
def db_session():
    return Session()
