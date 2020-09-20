from typing import List
from fastapi import FastAPI
from todo_app.schemas import Todo
from todo_app.uow import SqlAlchemyTodoUnitOfWork

from todo_app.services import (
    list_todo,
    add_todo,
    upsert_todo,
    delete_todo,
)

from todo_app.orm import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

uow = SqlAlchemyTodoUnitOfWork()


@app.get("/")
def todo_items():
    return list_todo(uow)


@app.post("/todo")
def todo_add(todo: Todo):
    return add_todo(uow, todo)


@app.put("/todo/{todo_id}")
def todo_upsert(todo_id: int, todo: Todo):
    return upsert_todo(uow, todo_id, todo)


@app.delete("/todo/{todo_id}")
def todo_delete(todo_id: int, uow):
    return delete_todo(uow, todo_id)
