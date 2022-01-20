import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def create_sessionmaker_engine():
    pg_user = os.environ.get("POSTGRES_USER")
    pg_password = os.environ.get("POSTGRES_PASSWORD")
    pg_host = os.environ.get("POSTGRES_HOST")
    pg_db = os.environ.get("POSTGRES_DB")
    DATABASE_URL = f"""postgresql://{pg_user}:{pg_password}@{pg_host}"""

    engine = create_engine(f"{DATABASE_URL}/{pg_db}")

    return sessionmaker(autocommit=False, autoflush=False, bind=engine), engine


Base = declarative_base()
