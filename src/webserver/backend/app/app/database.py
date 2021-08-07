import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta

pg_user = os.environ.get("POSTGRES_USER", "opensoar")
pg_password = os.environ.get("POSTGRES_PASSWORD", "password")
pg_host = os.environ.get("POSTGRES_HOST", "postgres.default.svc.cluster.local")
pg_db = os.environ.get("POSTGRES_DB", "opensoar")
DATABASE_URL = f"""postgresql://{pg_user}:{pg_password}@{pg_host}"""

engine = create_engine(f"{DATABASE_URL}/{pg_db}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()
