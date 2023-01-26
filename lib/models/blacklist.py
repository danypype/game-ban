from lib.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import validates

import re


class Blacklist(BaseModel):
    __tablename__ = 'blacklist'
    __table_args__ = (
        PrimaryKeyConstraint('game_id', 'email'),
    )

    game_id = Column(
        Integer, ForeignKey('games.id', ondelete='CASCADE'), index=True
    )
    email = Column(String(320), nullable=False, index=True)
    reason = Column(String(512), nullable=False, index=True)

    @validates('email')
    def validate_email(self, key, value):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if not re.fullmatch(regex, value):
            raise ValueError('invalid value for email')
        return value

    def to_dict(self):
        return {
            'game_id': self.game_id,
            'email': self.email,
            'reason': self.reason
        }
