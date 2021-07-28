import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

pg_user = os.environ.get("POSTGRES_USER", "opensoar")
pg_password = os.environ.get("POSTGRES_PASSWORD", "password")
pg_host = os.environ.get("POSTGRES_HOST", "postgres.default.svc.cluster.local")
pg_db = os.environ.get("POSTGRES_DB", "opensoar")
SQLALCHEMY_DATABASE_URL = f"""postgresql://{pg_user}:{pg_password}@{pg_host}"""

engine = create_engine(f"{SQLALCHEMY_DATABASE_URL}/{pg_db}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
