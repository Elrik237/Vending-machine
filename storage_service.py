from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model_snacks import ListOfSnacks


class StorageService:
    def __init__(self):
        self.sessions = {}

        self.engine = self.create_engine()
        self.create_tables(self.engine)

    def create_engine(self):
        engine = create_engine('sqlite:///list_of_snacks.db', echo=None)
        return engine

    def create_tables(self, engine):
        ListOfSnacks.metadata.create_all(self.engine)

    def create_session(self):
        session = sessionmaker(bind=self.engine)()
        return session
