from sqlalchemy.orm import session
from todo_app.orm import Todo
from todo_app.domain import schemas
import datetime

from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def add(self):
        ...

    @abstractmethod
    def get(self, id: int):
        ...

    @abstractmethod
    def delete(self, id: int):
        ...

    @abstractmethod
    def list(self):
        ...


class UpsertTodoMixin:
    def upsert(self, id: int, todo: schemas.Todo):
        old_todo = self.get(id)
        if old_todo:
            old_todo.title = todo.title
            old_todo.description = todo.description
            old_todo.completed = todo.completed
            old_todo.updated_at = datetime.datetime.now()
            return old_todo
        else:
            todo.id = id
            self.add(todo)
            return todo


class FakeRepository(AbstractRepository, UpsertTodoMixin):
    def __init__(self, db=list()):
        self.db = db
        self.counter = 1

    def add(self, todo: schemas.Todo):
        todo_model = Todo(**todo.dict())
        todo_model.id = self.counter
        self.counter += 1
        self.db.append(todo_model)
        return todo_model

    def get(self, todo_id: int):
        for item in self.db:
            if item.id == todo_id:
                return item
        else:
            return None

    def delete(self, todo_id: int):
        for todo in self.db:
            if todo.id == todo_id:
                break
        self.db.remove(todo)
        return todo

    def list(self):
        return self.db


class TodoRepository(AbstractRepository, UpsertTodoMixin):
    def __init__(self, session: session.Session):
        self.session = session

    def add(self, todo: schemas.Todo):
        todo_model = Todo(**todo.dict())
        self.session.add(todo_model)
        return todo_model

    def get(self, todo_id: int):
        return self.session.query(Todo).filter(Todo.id == todo_id).first()

    def delete(self, todo_id: int):
        todo = self.get(todo_id)
        if todo:
            self.session.delete(todo)
            return todo

    def list(self):
        return self.session.query(Todo).all()
