from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os

################### START UPs ###################

load_dotenv();

# Read variables from environment
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

#1st Get your URL
SQLMODEL_DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# STEP 2 BUILD MY ENGINE: responsible for sql alchemy to connect to the database
engine = create_async_engine(SQLMODEL_DATABASE_URL)