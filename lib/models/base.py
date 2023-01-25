from lib.db import Base
from sqlalchemy import Column, DateTime, text


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
