from lib.controllers import GameController
from lib.models import Game


def test_constructor(db_session):
    """
    Tests the instantiation of a GameController
    """
    controller = GameController(db_session)
    assert controller.session == db_session


def test_create_game(db_session):
    db_session.query(Game).delete()

    controller = GameController(db_session)
    game = controller.create_game(name='Call of Duty')

    assert isinstance(game.id, int)
    assert game.name == 'Call of Duty'

    created_game = db_session.query(Game).one()
    assert created_game.id == game.id


def test_find_game_by_id(db_session, create_game):
    db_session.query(Game).delete()
    game = create_game(name='Unreal Tournament')

    controller = GameController(db_session)
    found_game = controller.find_game_by_id(game.id)

    assert found_game == game


def test_find_all_games(db_session, create_game):
    db_session.query(Game).delete()

    games = [
        create_game(name='Unreal Tournament'),
        create_game(name='Halo Guardians'),
        create_game(name='Call of Duty')
    ]

    controller = GameController(db_session)
    found_games = controller.find_all_games()

    assert len(found_games) == 3
    assert set([game.id for game in found_games]) == set([game.id for game in games])
    assert set([game.name for game in found_games]) == set([game.name for game in games])
