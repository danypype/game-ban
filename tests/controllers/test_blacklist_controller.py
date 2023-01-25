from datetime import datetime, timedelta
from lib.controllers import BlacklistController
from lib.models import Game, Blacklist


def test_constructor(db_session):
    """
    Tests the instantiation of a BlacklistController
    """
    controller = BlacklistController(db_session)
    assert controller.session == db_session


def test_create_entry(db_session, create_game):
    """
    Tests the creation of a Blacklist entry
    """
    db_session.query(Game).delete()
    game = create_game(name='Call of Duty')

    controller = BlacklistController(db_session)
    black_list_entry = controller.create_entry(
        game_id=game.id,
        email='john.doe@example.com',
        reason='offensive_language'
    )

    created_entry = db_session.query(Blacklist).one()
    assert created_entry == black_list_entry


def test_find_by_game_id_and_email(db_session, create_game, create_blacklist_entry):
    """
    Tests retrieving a Blacklist entry by game_id and email
    """
    db_session.query(Game).delete()
    controller = BlacklistController(db_session)

    games = [
        create_game(name='Unreal Tournament'),
        create_game(name='Halo Guardians')
    ]
    black_list_entries = [
        create_blacklist_entry(
            game_id=games[0].id,
            email='john.doe@example.com',
            reason='terms_of_service_violation'
        ),
        create_blacklist_entry(
            game_id=games[1].id,
            email='richard.roe@example.com',
            reason='offensive_language'
        )
    ]

    found_entry = controller.find_by_game_id_and_email(
        game_id=games[0].id,
        email='john.doe@example.com',
    )
    assert found_entry == black_list_entries[0]

    found_entry = controller.find_by_game_id_and_email(
        game_id=games[1].id,
        email='richard.roe@example.com',
    )
    assert found_entry == black_list_entries[1]

    found_entry = controller.find_by_game_id_and_email(
        game_id=games[1].id,
        email='jane.doe@example.com',
    )
    assert found_entry is None


def test_get_report_for_player(db_session, create_game, create_blacklist_entry):
    """
    Tests the player report is generated with correct information
        and as per requirements
    """
    db_session.query(Game).delete()
    controller = BlacklistController(db_session)

    games = [
        create_game(name='Unreal Tournament'),
        create_game(name='Halo Guardians'),
        create_game(name='Call of Duty')
    ]
    create_blacklist_entry(
        game_id=games[0].id,
        email='john.doe@example.com',
        reason='terms_of_service_violation'
    )
    create_blacklist_entry(
        game_id=games[1].id,
        email='john.doe@example.com',
        reason='terms_of_service_violation'
    )
    create_blacklist_entry(
        game_id=games[2].id,
        email='john.doe@example.com',
        reason='offensive_language'
    )
    create_blacklist_entry(
        game_id=games[0].id,
        email='richard.roe@example.com',
        reason='terms_of_service_violation'
    )
    create_blacklist_entry(
        game_id=games[1].id,
        email='richard.roe@example.com',
        reason='offensive_language',
        created_at=datetime.now() - timedelta(days=91)
    )

    john_doe_report = controller.get_report_for_player(
        email='john.doe@example.com'
    )
    assert john_doe_report == {
        'most_common_reason': 'terms_of_service_violation',
        'times_reported_last_90_days': 3,
        'number_of_games_reported': 3
    }

    richard_roe_report = controller.get_report_for_player(
        email='richard.roe@example.com'
    )
    assert richard_roe_report == {
        'most_common_reason': 'terms_of_service_violation',
        'times_reported_last_90_days': 2,
        'number_of_games_reported': 2
    }

    jane_doe_report = controller.get_report_for_player(
        email='jane.doe@example.com'
    )
    assert jane_doe_report == {
        'most_common_reason': None,
        'times_reported_last_90_days': 0,
        'number_of_games_reported': 0
    }
