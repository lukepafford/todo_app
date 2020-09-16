from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from todo_app.schemas import Todo

from todo_app.services import (
    list_todo,
    add_todo,
    upsert_todo,
    delete_todo,
)

from todo_app.orm import engine, Base, get_session

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def todo_items(db: Session = Depends(get_db)):
    todo_items = list_todo(db)
    return todo_items


@app.post("/todo")
def todo_add(todo: Todo, db: Session = Depends(get_db)):
    return add_todo(db, todo)


@app.put("/todo/{todo_id}")
def todo_upsert(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    return upsert_todo(db, todo_id, todo)


@app.delete("/todo/{todo_id}")
def todo_delete(todo_id: int, db: Session = Depends(get_db)):
    return delete_todo(db, todo_id)
