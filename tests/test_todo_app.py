import pytest
from todo_app import __version__
from todo_app import schemas, orm
from todo_app.repository import FakeRepository


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture()
def schema():
    schema = schemas.Todo(id=1, title="test", description="test", completed=True)

    yield schema


def test_model_works(schema):
    todo = orm.Todo(**schema.dict())

    assert todo.id == 1
    assert todo.title == "test"
    assert todo.description == "test"
    assert todo.completed is True


def test_fake_repository(schema):
    repo = FakeRepository()
    repo.add(schema)
    s = repo.get(schema.id)

    assert s.id == schema.id

    repo.upsert(1, schema)
    assert len(repo.list()) == 1

    repo.upsert(2, schema)
    assert len(repo.list()) == 2

    repo.delete(schema.id)
    assert len(repo.list()) == 1
