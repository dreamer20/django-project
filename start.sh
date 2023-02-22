#!/bin/bash

if [ "$initial" = true ]; then
    echo "Start database migration."
    python3 manage.py migrate
    until python3 manage.py migrate
    do
        echo "Wait 3 seconds to try migration again."
        sleep 3
    done
fi
python3 manage.py runserver 0.0.0.0:8000