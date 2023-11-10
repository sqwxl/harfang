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

populate: rm-migrations migrate
    python3 manage.py setup_test_data

setup:
    pip3 install -r requirements.txt
    pre-commit install
    python3 manage.py makemigrations

rm-migrations:
    #!/usr/bin/env bash
    echo "Removing migrations..."
    find . -path "*/migrations/0*.py" -delete 2> /dev/null
    find . -path "*/migrations/__pycache__" -delete 2> /dev/null
    echo "Removing database..."
    rm -f db.sqlite3 2> /dev/null
