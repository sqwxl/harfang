FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=harfang.settings.prod
# ENV PYTHONPATH /app:$PYTHONPATH

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate && python manage.py collectstatic --noinput
