#! /usr/bin/env bash

# Let the DB start
python backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python initial_data.py

uvicorn app.main:app --host 0.0.0.0 --port 8080
