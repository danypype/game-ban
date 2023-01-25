from sqlalchemy.exc import IntegrityError
from lib.models import BaseModel, Game

import pytest


def test_game_model():
    """
    Makes sure the definition of the Game model is correct
    """
    assert issubclass(Game, BaseModel)
    assert hasattr(Game, 'name')


def test_to_dict(db_session):
    """
    Tests the method Game.to_dict making sure it returns a valid dict
    """
    db_session.query(Game).delete()
    game = Game(name='Halo Guardians')
    db_session.add(game)
    db_session.commit()

    game_dict = game.to_dict()
    assert 'id' in game_dict
    assert 'name' in game_dict
    assert isinstance(game_dict['id'], int)
    assert game_dict['name'] == 'Halo Guardians'


def test_create_game(db_session):
    """
    Tests the creation of a Game record
    """
    db_session.query(Game).delete()

    game = Game(name="Halo Guardians")
    db_session.add(game)
    db_session.commit()

    created_game = db_session.query(Game).one()
    assert created_game.id is not None
    assert created_game.name == "Halo Guardians"


def test_create_duplicate_game(db_session):
    """
    Ensures the code fails when trying to create a duplicate game
    """
    db_session.query(Game).delete()

    game = Game(name="Halo Guardians")
    db_session.add(game)
    db_session.commit()

    game_count = db_session.query(Game).count()
    assert game_count == 1

    with pytest.raises(IntegrityError):
        game = Game(name="Halo Guardians")
        db_session.add(game)
        db_session.commit()
