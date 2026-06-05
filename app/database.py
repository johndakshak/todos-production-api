from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_CONNECTION = os.getenv('DB_CONNECTION', 'postgresql')

# SQLALCHEMY_DB_URL = f'{DB_CONNECTION}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
SQLALCHEMY_DB_URL = f'postgresql://postgres.kxxalvotibavtndxgnsv:N!ga7GL,s+Y-6Vd@aws-1-eu-central-1.pooler.supabase.com:5432/postgres'
print(SQLALCHEMY_DB_URL)

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