from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.todo import Todo
from schema.guest_schema import GuestTodoCreate, GuestTodoResponse
from enums import TodoStatus

router = APIRouter(prefix="/guest", tags=["Guest"])

@router.get("/todos", response_model=list[GuestTodoResponse])
def get_public_guest_todos(db: Session = Depends(get_db)):
    """Get all public todos created by guests (accessible without authentication)"""
    todos = db.query(Todo).filter(Todo.is_public == True, Todo.user_id == None).all()
    return todos

@router.post("/todos", response_model=GuestTodoResponse)
def create_guest_todo(todo: GuestTodoCreate, db: Session = Depends(get_db)):
    """Create a todo as a guest (no authentication required)"""
    new_todo = Todo(
        description=todo.description,
        is_public=todo.is_public,
        user_id=None,  
        guest_name=todo.guest_name,
        status=TodoStatus.pending
    )
    
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo
