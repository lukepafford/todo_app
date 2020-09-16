from sqlalchemy.orm import Session
from todo_app.repository import TodoRepository
from todo_app import schemas


def list_todo(db: Session):
    repo = TodoRepository(db)
    todo_items = repo.list()
    return todo_items


def add_todo(db: Session, todo: schemas.Todo):
    repo = TodoRepository(db)
    repo.add(todo)
    db.commit()


def upsert_todo(db: Session, todo_id: int, todo: schemas.Todo):
    repo = TodoRepository(db)
    old_todo = repo.get(todo_id)
    repo.upsert(todo_id, todo)
    db.commit()


def delete_todo(db: Session, todo_id: int):
    repo = TodoRepository(db)
    repo.delete(todo_id)
    db.commit()
