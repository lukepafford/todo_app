dev:
	uvicorn main:app --reload

test:
	pytest --cov=todo_app/ --cov-branch --cov-report=term-missing
