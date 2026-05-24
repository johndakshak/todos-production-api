from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enums import TodoStatus

class GuestTodoCreate(BaseModel):
    description: str = Field(min_length=1, max_length=500)
    guest_name: Optional[str] = Field(default=None, min_length=0, max_length=30)
    is_public: bool = True

class GuestTodoResponse(BaseModel):
    id: int
    guest_name: Optional[str] = Field(default=None, min_length=0, max_length=30)
    description: str
    is_public: bool
    status: TodoStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class GuestTodoStatusUpdate(BaseModel):
    status: TodoStatus

    model_config = {"from_attributes": True}


