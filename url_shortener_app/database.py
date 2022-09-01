from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .configuration import get_settings

'''
engine is the entry point to our database.
With this connection argument, SQLite allows more than one request at a time to communicate with the database.
'''
engine = create_engine(
    get_settings().db_url, connect_args={"check_same_thread": False}
)
'''
We create a working database session when we instantiate SessionLocal
'''
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
'''
The declarative_base function returns a class that connects the database engine to the SQLAlchemy functionality of the model.   
'''
Base = declarative_base()