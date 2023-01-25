from lib.models import Game


class GameController:
    """
    Game controller class. Interacts with the Game model
    """
    def __init__(self, session):
        """
        :param session: SQLAlchemy Session object
        """
        self.session = session

    def create_game(self, name):
        """
        Creates a Game record

        :param name: String. Name of the game
        :return: Created game object
        """
        game = Game(name=name)
        self.session.add(game)
        self.session.commit()
        return game

    def find_game_by_id(self, game_id):
        """
        Finds a Game record by id

        :param game_id: ID of the game to find
        :return: Found Game record. None if not found
        """
        return self.session.query(Game).filter(
            Game.id == game_id
        ).one_or_none()

    def find_all_games(self):
        """
        :return: A list containing all Game records
        """
        return self.session.query(Game).all()
