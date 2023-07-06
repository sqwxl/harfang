serve:
  pythonh manage.py migrate
  python manage.py runserver

css:
  tailwindcss -i newsapp/static/newsapp/css/input.css -o newsapp/static/newsapp/css/output.css --watch
