from typing import List
from fastapi import FastAPI, Depends
from todo_app.domain.schemas import Todo
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


def uow():
    uow = SqlAlchemyTodoUnitOfWork()
    with uow:
        yield uow


@app.get("/", response_model=List[Todo])
def todo_items(uow=Depends(uow)):
    return list_todo(uow)


@app.post("/todo", response_model=Todo)
def todo_add(todo: Todo, uow=Depends(uow)):
    return add_todo(uow, todo)


@app.put("/todo/{todo_id}", response_model=Todo)
def todo_upsert(todo_id: int, todo: Todo, uow=Depends(uow)):
    return upsert_todo(uow, todo_id, todo)


@app.delete("/todo/{todo_id}", response_model=Todo)
def todo_delete(todo_id: int, uow=Depends(uow)):
    return delete_todo(uow, todo_id)
