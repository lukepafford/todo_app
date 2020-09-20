import pytest
from todo_app import __version__
from todo_app import schemas, orm
from todo_app.repository import FakeRepository
from todo_app.uow import FakeTodoUnitOfWork
from todo_app.services import list_todo, add_todo, upsert_todo, delete_todo


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture()
def todo_item():
    todo_item = schemas.Todo(id=1, title="test", description="test", completed=True)

    yield todo_item


@pytest.fixture()
def todo_items():
    todo_item1 = schemas.Todo(id=2, title="test", description="test", completed=True)
    todo_item2 = schemas.Todo(id=3, title="test", description="test", completed=True)
    todo_item3 = schemas.Todo(id=4, title="test", description="test", completed=True)

    yield [todo_item1, todo_item2, todo_item3]


@pytest.fixture()
def fake_uow(todo_items):
    uow = FakeTodoUnitOfWork(todo_items)
    yield uow


def test_model_works(todo_item):
    todo = orm.Todo(**todo_item.dict())

    assert todo.id == 1
    assert todo.title == "test"
    assert todo.description == "test"
    assert todo.completed is True


def test_fake_repository(todo_item):
    repo = FakeRepository()
    repo.add(todo_item)
    t = repo.get(todo_item.id)

    assert t.id == todo_item.id

    repo.upsert(1, todo_item)
    assert len(repo.list()) == 1

    repo.upsert(2, todo_item)
    assert len(repo.list()) == 2

    repo.delete(todo_item.id)
    assert len(repo.list()) == 1


def test_list_todo(fake_uow):
    assert len(list_todo(fake_uow)) == 3


def test_add_todo(fake_uow, todo_item):
    add_todo(fake_uow, todo_item)
    assert len(list_todo(fake_uow)) == 4


def test_delete_todo(fake_uow, todo_items):
    delete_todo(fake_uow, todo_items[0].id)
    assert len(list_todo(fake_uow)) == 2


def test_upsert_todo(fake_uow, todo_items):
    todo_item = todo_items[0]
    upsert_todo(fake_uow, todo_item.id, todo_item)
    assert len(list_todo(fake_uow)) == 3
