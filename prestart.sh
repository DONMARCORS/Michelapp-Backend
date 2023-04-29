#! /usr/bin/env bash
rm -rf ./alembic/versions/*
rm -rf ./alembic/versions/__pycache__


# Let the DB start
python3 ./app/backend_prestart.py

# Run migrations

alembic revision --autogenerate -m "first migration"

alembic upgrade head


# Create initial data in DB
python3 ./app/initial_data.py