from sqlalchemy import Column, DateTime, text
from lib.db import Base


class BaseModel(Base):
    """
    Abstract BaseModel class
    - Stores TIMESTAMP WITH TIMEZONE for created_at and updated_at
    - Makes sure the database sets updated_at = CURRENT_TIMESTAMP
        on update
    """
    __abstract__ = True

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )
