#!/bin/sh
alembic upgrade head
uvicorn --host 0.0.0.0 --port 8003 main:app
