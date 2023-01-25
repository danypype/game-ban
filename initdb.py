from lib.db import engine, Base
from lib.models import *

if __name__ == '__main__':
    Base.metadata.create_all(engine)
