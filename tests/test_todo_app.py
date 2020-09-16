from todo_app import __version__
from todo_app import schemas, orm


def test_version():
    assert __version__ == "0.1.0"


def test_model_works():
    schema = schemas.Todo(title="test", description="test", completed=True)
    todo = orm.Todo(**schema.dict())

    assert todo.title == "test"
    assert todo.description == "test"
    assert todo.completed is True
