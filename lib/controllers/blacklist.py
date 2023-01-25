from lib.models import Blacklist
from datetime import datetime, timedelta


class BlacklistController:
    """
    Blacklist controller class. Interacts with the Blacklist model
    """
    def __init__(self, session):
        """
        :param session: SQLAlchemy Session object
        """
        self.session = session

    def create_entry(self, game_id, email, reason):
        """
        Adds an entry to the blacklist

        :param game_id: Integer
        :param email: String. Email for the player to ban
        :param reason: String. Reason for the ban
        :return: Created Blacklist entry
        """
        black_list_entry = Blacklist(
            game_id=game_id,
            email=email,
            reason=reason
        )
        self.session.add(black_list_entry)
        self.session.commit()
        return black_list_entry

    def find_by_game_id_and_email(self, game_id, email):
        """
        Finds a Blacklist entry by game_id and email

        :return: The found Blacklist entry. None if not found
        """
        return self.session.query(Blacklist).filter(
            Blacklist.game_id == game_id,
            Blacklist.email == email
        ).one_or_none()

    def get_report_for_player(self, email):
        """
        Generates a report with information about the given player in the blacklist

        :param email: String. Email of the player to generate the report for
        :return: Dictionary with report data
            {
                "most_common_reason": String. Most common ban reason the player has been banned for
                "times_reported_last_90_days": Integer. Times the player was banned in the last 90 days
                "number_of_games_reported": Integer. Number of games the player has been banned for
            }
        """
        black_list_entries = self.session.query(Blacklist).filter(
            Blacklist.email == email
        ).all()

        if not black_list_entries:
            return {
                "most_common_reason": None,
                "times_reported_last_90_days": 0,
                "number_of_games_reported": 0
            }

        reason_count = {}
        times_reported_last_90_days = 0
        ninety_days_ago = datetime.now() - timedelta(days=90)
        number_of_games_reported = 0

        for entry in black_list_entries:
            reason_count[entry.reason] = reason_count.get(entry.reason, 0)
            reason_count[entry.reason] += 1

            created_at = entry.created_at
            if created_at > ninety_days_ago:
                times_reported_last_90_days += 1

            number_of_games_reported += 1

        most_common_reason = (None, 0)

        for reason, count in reason_count.items():
            mc_reason, mc_count = most_common_reason
            if count > mc_count:
                most_common_reason = (reason, count)

        return {
            'most_common_reason': most_common_reason[0],
            'times_reported_last_90_days': times_reported_last_90_days,
            'number_of_games_reported': number_of_games_reported
        }
