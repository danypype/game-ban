from datetime import datetime, timedelta

import os

api_key = os.environ['API_KEY']


def test_create_game(api_client):
    """
    Tests the creation of a Game record through the API
    """
    response = api_client.post('/games?api_key=invalid-key')
    assert response.status_code == 401

    response = api_client.post(
        f'/games?api_key={api_key}',
        json={'name': ''}
    )
    assert response.status_code == 400
    assert response.json == {'message': 'name is required'}

    response = api_client.post(
        f'/games?api_key={api_key}',
        json={'name': 'Unreal Tournament'}
    )
    assert response.status_code == 201
    assert isinstance(response.json['id'], int)
    assert response.json['name'] == 'Unreal Tournament'


def test_fetch_games(api_client, db_session, create_game):
    """
    Tests retrieving Game records through the API
    """
    games = [
        create_game(name='Game 1'),
        create_game(name='Game 2')
    ]

    response = api_client.get(f'/games?api_key={api_key}')
    data = response.json

    assert response.status_code == 200
    assert len(data) == 2
    assert games[0].to_dict() in data
    assert games[1].to_dict() in data


def test_append_to_blacklist(api_client, create_game):
    """
    Tests adding an entry to the Blacklist
    """
    game = create_game(name='Halo Guardians')

    # request without game_id
    response = api_client.post(
        f'/blacklist?api_key={api_key}',
        json={
            'email': 'john.doe@example.com',
            'reason': 'unwanted_behavior'
        }
    )
    assert response.status_code == 400
    assert response.json == {'message': 'game_id is required'}

    # request without email
    response = api_client.post(
        f'/blacklist?api_key={api_key}',
        json={
            'game_id': game.id,
            'reason': 'unwanted_behavior'
        }
    )
    assert response.status_code == 400
    assert response.json == {'message': 'email is required'}

    # request with invalid email
    response = api_client.post(
        f'/blacklist?api_key={api_key}',
        json={
            'game_id': game.id,
            'email': 'john.doe@',
            'reason': 'unwanted_behavior'
        }
    )
    assert response.status_code == 400
    assert response.json == {'message': 'invalid value for email'}

    # valid request
    response = api_client.post(
        f'/blacklist?api_key={api_key}',
        json={
            'game_id': game.id,
            'email': 'john.doe@example.com',
            'reason': 'unwanted_behavior'
        }
    )
    assert response.status_code == 201
    assert response.json == {
        'game_id': game.id,
        'email': 'john.doe@example.com',
        'reason': 'unwanted_behavior'
    }

    # request with duplicate entry
    response = api_client.post(
        f'/blacklist?api_key={api_key}',
        json={
            'game_id': game.id,
            'email': 'john.doe@example.com',
            'reason': 'unwanted_behavior'
        }
    )
    assert response.status_code == 400
    assert response.json == {
        'message': f'player john.doe@example.com is already black-listed for game_id {game.id}'
    }


def test_check_blacklist(api_client, create_game, create_blacklist_entry):
    """
    Tests retrieving information about a player in the Blacklist,
        as per requirements
    """
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
        reason='offensive_language',
        created_at=datetime.now() - timedelta(days=91)
    )

    response = api_client.get(f'/blacklist/check?api_key={api_key}')
    assert response.status_code == 400
    assert response.json == {'message': 'email must be provided'}

    response = api_client.get(
        f'/blacklist/check?email=jane.doe@example.com&api_key={api_key}'
    )
    assert response.status_code == 404
    assert response.json == {'message': 'email not found'}

    response = api_client.get(
        f'/blacklist/check?email=john.doe@example.com&api_key={api_key}'
    )
    assert response.status_code == 200
    assert response.json == {
        'most_common_reason': 'terms_of_service_violation',
        'number_of_games_reported': 3,
        'times_reported_last_90_days': 2
    }
