from sqlalchemy.exc import IntegrityError
from lib.models import BaseModel, Game, Blacklist

import pytest


def test_blacklist_model():
    """
    Makes sure the definition of the Blacklist model is correct
    """
    assert issubclass(Blacklist, BaseModel)
    assert hasattr(Blacklist, 'game_id')
    assert hasattr(Blacklist, 'email')
    assert hasattr(Blacklist, 'reason')

