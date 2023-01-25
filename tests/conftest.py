from lib.db import Session
from lib.models import Game, Blacklist

import pytest


@pytest.fixture
def db_session():
    return Session()


@pytest.fixture
def create_game(db_session):
    def wrapper(name):
        game = Game(name=name)
        db_session.add(game)
        db_session.commit()
        return game
    return wrapper


@pytest.fixture
def create_blacklist_entry(db_session):
    def wrapper(game_id, email, reason, created_at=None):
        black_list_entry = Blacklist(
            game_id=game_id,
            email=email,
            reason=reason
        )

        if created_at:
            black_list_entry.created_at = created_at

        db_session.add(black_list_entry)
        db_session.commit()
        return black_list_entry

    return wrapper
