#!/bin/bash

if [ "$initial" = true ]; then
    python3 manage.py migrate
    python3 manage.py runserver 0.0.0.0:8000
else
    python3 manage.py runserver 0.0.0.0:8000
fi