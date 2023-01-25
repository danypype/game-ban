from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from lib.db import Session
from lib.controllers import GameController, BlacklistController


app = Flask(__name__)
session = Session()


@app.route('/games', methods=['POST'])
def create_game():
    """
    Creates a game

    request payload:
        {"name": String}
    response example:
        {"id":1,"name":"Halo Guardians"}
    """
    body = request.json

    if not body.get('name'):
        return jsonify({"message": "name is required"}), 400

    game = GameController(session).create_game(name=body['name'])
    return jsonify(game.to_dict()), 201


@app.route('/games', methods=['GET'])
def fetch_games():
    """
    Retrieves all games

    response example:
         [{"id":1,"name":"Halo Guardians"},{"id":2,"name":"Call of Duty"}]
    """
    games = GameController(session).find_all_games()
    return jsonify([game.to_dict() for game in games]), 200


@app.route('/blacklist', methods=['POST'])
def append_to_blacklist():
    """
    Adds an entry in the blacklist for the given player and game

    response example:
         {"email":"john.doe@example.com","game_id":1,"reason":"offensive_language"}
    """
    body = request.json

    if not body.get('game_id'):
        return jsonify({"message": "game_id is required"}), 400
    if not body.get('email'):
        return jsonify({"message": "email is required"}), 400
    if not body.get('reason'):
        return jsonify({"message": "reason is required"}), 400

    game_id = body['game_id']
    email = body['email']
    reason = body['reason']

    game = GameController(session).find_game_by_id(game_id)

    if game is None:
        raise NotFound('game_id not found')

    black_list_controller = BlacklistController(session)
    black_list_entry = black_list_controller.find_by_game_id_and_email(
        game_id=game_id,
        email=email
    )

    if black_list_entry:
        return jsonify({
            'message': f'player {email} is already black-listed for game_id {game_id}'
        }), 400

    black_list_entry = black_list_controller.create_entry(
        game_id=game_id,
        email=email,
        reason=reason
    )
    return jsonify(black_list_entry.to_dict()), 201


@app.route('/blacklist/check', methods=['GET'])
def check_blacklist():
    """
    Retrieves information about a given player in the blacklist

    request arguments:
        - email: The email to search for
    response:
        {
            "most_common_reason": String. Most common ban reason
            "times_reported_last_90_days": Integer. Times the player was banned in the last 90 days
            "number_of_games_reported": Integer. Number of games the player has been banned for
        }
    """
    args = request.args
    email = args.get('email')

    if not email:
        return jsonify({"message": "email must be provided"}), 400

    report = BlacklistController(session).get_report_for_player(email=email)

    if not report['number_of_games_reported']:
        return jsonify({"message": "Email not found"}), 404

    return jsonify(report), 200
