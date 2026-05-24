from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_CONNECTION = os.getenv('DB_CONNECTION', 'mysql')

# Support both MySQL and PostgreSQL
if DB_CONNECTION == 'postgresql':
    SQLALCHEMY_DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
else:
    SQLALCHEMY_DB_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

engine = create_engine(SQLALCHEMY_DB_URL, echo=True)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = Session()

    try:
        yield db
    finally:
        db.close()

