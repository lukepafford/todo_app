from todo_app.uow import AbstractUnitOfWork
from todo_app import schemas


def list_todo(uow: AbstractUnitOfWork):
    with uow:
        return uow.todo_items.list()


def add_todo(uow: AbstractUnitOfWork, todo: schemas.Todo):
    with uow:
        uow.todo_items.add(todo)
        uow.commit()


def upsert_todo(uow: AbstractUnitOfWork, todo_id: int, todo: schemas.Todo):
    with uow:
        uow.todo_items.upsert(todo_id, todo)
        uow.commit()


def delete_todo(uow: AbstractUnitOfWork, todo_id: int):
    with uow:
        uow.todo_items.delete(todo_id)
        uow.commit()
