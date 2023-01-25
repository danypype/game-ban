from lib.models.base import BaseModel
from sqlalchemy import Column, Integer, String


class Game(BaseModel):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name}
