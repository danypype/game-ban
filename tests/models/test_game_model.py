from datetime import datetime
from sqlalchemy.exc import IntegrityError
from lib.models import BaseModel, Game

import pytest


def test_game_model():
    """
    Makes sure the definition of the Game model is correct
    """
    assert issubclass(Game, BaseModel)
    assert hasattr(Game, 'name')


def test_create_game(db_session):
    """
    Tests the creation of a Game record
    """
    game = Game(name="Halo Guardians")
    db_session.add(game)
    db_session.commit()

    game_entry = db_session.query(Game).one()
    assert isinstance(game_entry.created_at, datetime)
    assert isinstance(game_entry.created_at, datetime)

    entry_dict = game_entry.to_dict()
    assert entry_dict['id'] == game_entry.id
    assert entry_dict['name'] == 'Halo Guardians'


def test_create_duplicate_game(db_session):
    """
    Ensures the code fails when trying to create a duplicate game
    """
    game = Game(name="Halo Guardians")
    db_session.add(game)
    db_session.commit()

    with pytest.raises(IntegrityError):
        game = Game(name="Halo Guardians")
        db_session.add(game)
        db_session.commit()

    db_session.rollback()
