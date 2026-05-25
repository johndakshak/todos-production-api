from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.todo import Todo
from app.models.user import User
from app.schema.todo_schema import TodoCreate, TodoResponse, TodoUpdate
from app.middleware.auth import JWTBearer
from typing import Optional
from app.enums import TodoStatus

router = APIRouter(prefix="/todos", tags=["Todos"])

def get_current_user_or_none(token: str = Depends(JWTBearer(auto_error=False))) -> Optional[User]:
    """Helper to get current user or None if not authenticated"""
    return token

@router.get("/my-todos", response_model=list[TodoResponse])
def get_my_todos(db: Session = Depends(get_db), current_user: User = Depends(JWTBearer())):
    """Get all todos belonging to the logged-in user (requires authentication)"""
    todos = db.query(Todo).filter(Todo.user_id == current_user.id).all()
    return todos

@router.get("/", response_model=list[TodoResponse])
def get_todos(db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user_or_none)):
    """
    Get todos based on authentication:
    - Guest (not logged in): Only public todos
    - Logged in: Public todos + own private todos
    """
    if current_user:
        # Logged in: get public todos + own private todos
        todos = db.query(Todo).filter(
            (Todo.is_public == True) | (Todo.user_id == current_user.id)
        ).all()
    else:
        # Guest: only public todos
        todos = db.query(Todo).filter(Todo.is_public == True).all()
    
    return todos

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user_or_none)):
    """Get a specific todo if visible to the user"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Check visibility
    if not todo.is_public and (not current_user or todo.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Access denied: Private todo")
    
    return todo

@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(JWTBearer())):
    """Create a new todo (requires authentication)"""
    new_todo = Todo(
        description=todo.description,
        is_public=todo.is_public,
        user_id=current_user.id,
        guest_name=None
    )
    
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_data: TodoUpdate, db: Session = Depends(get_db), current_user: User = Depends(JWTBearer())):
    """Update a todo (only owner can update)"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: Not your todo")
    
    for field, value in todo_data.model_dump(exclude_unset=True).items():
        setattr(todo, field, value)
    
    db.commit()
    db.refresh(todo)
    
    return todo

@router.patch("/{todo_id}", response_model=TodoResponse)
def patch_todo(todo_id: int, todo_data: TodoUpdate, db: Session = Depends(get_db), current_user: User = Depends(JWTBearer())):
    """Partially update a todo (only owner can update)"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: Not your todo")
    
    for field, value in todo_data.model_dump(exclude_unset=True).items():
        setattr(todo, field, value)
    
    db.commit()
    db.refresh(todo)
    
    return todo

@router.patch("/{todo_id}/complete", response_model=TodoResponse)
def mark_todo_completed(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(JWTBearer())):
    """Mark a todo as completed (only owner can mark)"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: Not your todo")
    
    todo.status = TodoStatus.completed
    
    db.commit()
    db.refresh(todo)
    
    return todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(JWTBearer())):
    """Delete a todo (only owner can delete)"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: Not your todo")
    
    db.delete(todo)
    db.commit()
    
    return {"detail": f"Todo {todo_id} deleted successfully"}
