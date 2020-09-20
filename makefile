dev:
	uvicorn main:app --reload

test:
	pytest -v --cov=todo_app/ --cov-branch --cov-report=term-missing
