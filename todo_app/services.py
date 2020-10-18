from todo_app.uow import AbstractUnitOfWork
from todo_app.domain import schemas


def list_todo(uow: AbstractUnitOfWork):
    return uow.todo_items.list()


def add_todo(uow: AbstractUnitOfWork, todo: schemas.Todo):
    added_todo = uow.todo_items.add(todo)
    uow.commit()

    return added_todo


def upsert_todo(uow: AbstractUnitOfWork, todo_id: int, todo: schemas.Todo):
    upserted_todo = uow.todo_items.upsert(todo_id, todo)
    uow.commit()

    return upserted_todo


def delete_todo(uow: AbstractUnitOfWork, todo_id: int):
    deleted_todo = uow.todo_items.delete(todo_id)
    uow.commit()

    return deleted_todo
