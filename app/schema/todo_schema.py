from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.enums import TodoStatus

class TodoCreate(BaseModel):
    description: str = Field(min_length=1, max_length=500)
    is_public: bool = False

class TodoResponse(BaseModel):
    id: int
    description: str
    is_public: bool
    user_id: Optional[int] = None
    status: TodoStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class TodoUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    is_public: Optional[bool] = None
    status: Optional[TodoStatus] = None

    model_config = {"from_attributes": True}
