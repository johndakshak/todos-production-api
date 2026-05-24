from database import engine
from models.base import Base
from models.user import User
from models.todo import Todo

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
