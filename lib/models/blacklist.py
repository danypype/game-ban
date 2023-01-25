from lib.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint


class Blacklist(BaseModel):
    __tablename__ = 'blacklist'
    __table_args__ = (
        PrimaryKeyConstraint('game_id', 'email'),
    )

    game_id = Column(Integer, ForeignKey('games.id'))
    email = Column(String(320), nullable=False, index=True)
    reason = Column(String(512), nullable=False, index=True)

    def to_dict(self):
        return {
            'game_id': self.game_id,
            'email': self.email,
            'reason': self.reason
        }
