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
    db_session.query(Game).delete()

    game = Game(name="Halo Guardians")
    db_session.add(game)
    db_session.commit()

    game_entry = db_session.query(Game).one()
    entry_dict = game_entry.to_dict()

    assert isinstance(entry_dict['id'], int)
    assert entry_dict['name'] == 'Halo Guardians'


def test_create_duplicate_game(db_session):
    """
    Ensures the code fails when trying to create a duplicate game
    """
    db_session.query(Game).delete()

    game = Game(name="Halo Guardians")
    db_session.add(game)
    db_session.commit()

    with pytest.raises(IntegrityError):
        game = Game(name="Halo Guardians")
        db_session.add(game)
        db_session.commit()

    db_session.rollback()
