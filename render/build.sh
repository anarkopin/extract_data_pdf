#!/bin/bash

#Exit an error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

