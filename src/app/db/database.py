from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
import os

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/menu_db"

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal = sessionmaker(autocommit=False,
#                             autoflush=False,
#                             bind=engine)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()

database = Database(DATABASE_URL)
