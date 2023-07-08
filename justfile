serve:
  python manage.py migrate
  python manage.py runserver

css:
  tailwindcss -i newsapp/static/newsapp/css/input.css -o newsapp/static/newsapp/css/output.css --watch

populate:
  python manage.py setup_test_data

setup:
  #!/usr/bin/env bash
  if [ ! -d ".venv" ]; then
    python3 -m venv .venv
  elif [ -z "$VIRTUAL_ENV" ]; then
    echo "Please activate your virtualenv"
    exit 1
  fi
  pip install -r requirements.txt
  python manage.py makemigrations
