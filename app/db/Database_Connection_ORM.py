from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

Base = declarative_base()

class DatabaseConnectionORM:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.db = os.environ.get('DB_DB')
        try:
            connect_args = {
                'client_encoding': 'utf8',
                'options': '-c search_path=public',
                'application_name': 'MediosMagneticos'
            }
            
            self.engine = create_engine(
                f'postgresql+psycopg2://{self.user}:{quote_plus(self.password)}@{self.host}/{self.db}',
                connect_args=connect_args
            )
        except Exception as e:
            print(f'Error connecting: {e}')

    def get_base(self):
        return Base
    
    def get_engine(self):
        return self.engine

    def get_session(self): 
        Session = sessionmaker(bind=self.engine)
        return Session()
    
    def close(self):
        self.engine.dispose()