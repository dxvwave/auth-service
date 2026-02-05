export PYTHONPATH := "src"

run:
    uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

run-docker:
    docker-compose up --build

db-migrate:
    alembic upgrade head

db-revision name:
    alembic revision --autogenerate -m "{{name}}"
