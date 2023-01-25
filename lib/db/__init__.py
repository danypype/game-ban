from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

import os

Base = declarative_base()


engine = create_engine(
    os.environ['SQLALCHEMY_DATABASE_URI'],
    echo=os.environ['SQLALCHEMY_ECHO'].lower() in ('true', '1')
)
Session = sessionmaker(engine)
Session.configure(bind=engine)
