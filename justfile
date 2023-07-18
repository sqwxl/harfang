serve:
  python3 manage.py migrate
  python3 manage.py runserver

css:
  tailwindcss -i newsapp/static/newsapp/css/input.css -o newsapp/static/newsapp/css/output.css --watch

migrate:
  python3 manage.py makemigrations
  python3 manage.py migrate

populate:
  python3 manage.py setup_test_data

setup:
  pip3 install -r requirements.txt
  pre-commit install
  python3 manage.py makemigrations

clean:
  #!/usr/bin/env bash
  rm -r ./**/migrations/{0*.py,__pycache__} db.sqlite3
