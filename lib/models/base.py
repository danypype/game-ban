from datetime import datetime
from sqlalchemy import Column, DateTime, text
from lib.db import Base


class BaseModel(Base):
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
        onupdate=datetime.now
    )
