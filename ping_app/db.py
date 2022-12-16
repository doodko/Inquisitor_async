from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ping_app.models import Base
from settings_reader import config


engine = create_engine(config.db)
Session = sessionmaker(engine)


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
