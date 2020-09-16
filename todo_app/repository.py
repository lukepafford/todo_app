from sqlalchemy.orm import session
from todo_app.orm import Todo
from todo_app import schemas
import datetime


class TodoRepository:
    def __init__(self, session: session.Session):
        self.session = session

    def add(self, todo: schemas.Todo):
        todo_model = Todo(**todo.dict())
        self.session.add(todo_model)

    def get(self, todo_id: int):
        return self.session.query(Todo).filter(Todo.id == todo_id).first()

    def delete(self, todo_id: int):
        todo = self.get(todo_id)
        if todo:
            self.session.delete(todo)

    def upsert(self, todo_id: int, todo: schemas.Todo):
        old_todo = self.get(todo_id)
        if old_todo:
            old_todo.title = todo.title
            old_todo.description = todo.description
            old_todo.completed = todo.completed
            old_todo.updated_at = datetime.datetime.now()
        else:
            old_todo = Todo(**todo.dict())
            old_todo.id = todo_id

        self.session.add(old_todo)

    def list(self):
        return self.session.query(Todo).all()
