#! /usr/bin/env bash

set -e
set -x

while !</dev/tcp/db/5432; 
    do sleep 1;
done;

#alembic revision --autogenerate
#alembic upgrade head

uvicorn main:app --host 0.0.0.0