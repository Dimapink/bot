from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from utils.config import settings


engine = create_engine(url=settings.data_base_url, echo=True)
Session = sessionmaker(engine)
Base = declarative_base()


class Database:
    @staticmethod
    def create_tables():
        if not database_exists(engine.url):
            create_database(engine.url)
        with Session():
            Base.metadata.create_all(engine)
