from .orm import get_session
from .repository import TodoRepository, AbstractRepository, FakeRepository

from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    todo_items: AbstractRepository

    def __enter__(self, *args):
        pass

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        ...

    @abstractmethod
    def rollback(self):
        ...


class FakeTodoUnitOfWork(AbstractUnitOfWork):
    def __init__(self, items=list()):
        self.todo_items = FakeRepository(items)
        self.committed = False

    def __enter__(self):
        pass

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class SqlAlchemyTodoUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=get_session):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.todo_items = TodoRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
