#!/bin/sh
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
python3 -m flask run --host=0.0.0.0
