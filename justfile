serve:
    tailwindcss -i static/css/input.css -o static/css/output.css
    python3 manage.py migrate
    python3 manage.py runserver

run-containers:
    podman build -t harfang -f Dockerfile .
    podman-compose up -d

css:
    tailwindcss -i static/css/input.css -o static/css/output.css --watch

migrate:
    python3 manage.py makemigrations
    python3 manage.py migrate

populate: migrate
    python3 manage.py setup_test_data

setup:
    pip3 install -r requirements.txt
    pre-commit install
    python3 manage.py makemigrations

rm-migrations:
    #!/usr/bin/env bash
    rm -r ./**/migrations/{0*.py,__pycache__} db.sqlite3
