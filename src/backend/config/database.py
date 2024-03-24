from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_POSTGRES_HOST")
DB_PORT = int(os.getenv("DB_POSTGRES_PORT"))
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME=os.getenv("POSTGRES_DB_NAME")

if DB_NAME is None:
   DB_NAME=""

connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(connection_string)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
