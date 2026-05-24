from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, func
from models.base import Base
from sqlalchemy.orm import relationship
from enums import TodoStatus

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    guest_name = Column(String(50), nullable=True)
    description = Column(String(500), nullable=False)
    is_public = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    status = Column(Enum(TodoStatus), nullable=False, default=TodoStatus.pending.value, server_default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    user = relationship("User", back_populates="todos")
