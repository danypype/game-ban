from datetime import datetime
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


def test_create_blacklist_entry(db_session, create_game):
    """
    Takes the creation of a Blacklist method
    """
    db_session.query(Game).delete()
    game_entry = create_game(name='Halo Guardians')

    black_list = Blacklist(
        game_id=game_entry.id,
        email='john.doe@example.com',
        reason='terms_of_service_violation',
    )
    db_session.add(black_list)
    db_session.commit()

    black_list_entry = db_session.query(Blacklist).one()
    assert isinstance(black_list_entry.created_at, datetime)
    assert isinstance(black_list_entry.updated_at, datetime)

    entry_dict = black_list_entry.to_dict()
    assert entry_dict['game_id'] == game_entry.id
    assert entry_dict['email'] == 'john.doe@example.com'
    assert entry_dict['reason'] == 'terms_of_service_violation'


def test_create_duplicate_blacklist_entry(db_session):
    """
    Ensures the code fails when trying to create a duplicate Blacklist entry
    """
    db_session.query(Game).delete()

    game_entry = Game(name='Halo Guardians')
    db_session.add(game_entry)
    db_session.commit()

    black_list_entry = Blacklist(
        game_id=game_entry.id,
        email='john.doe@example.com',
        reason='terms_of_service_violation',
    )
    db_session.add(black_list_entry)
    db_session.commit()

    with pytest.raises(IntegrityError):
        black_list_entry = Blacklist(
            game_id=game_entry.id,
            email='john.doe@example.com',
            reason='terms_of_service_violation',
        )
        db_session.add(black_list_entry)
        db_session.commit()

    db_session.rollback()
