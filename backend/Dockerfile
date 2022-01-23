FROM python:3.7-slim

WORKDIR /app

COPY ./ /app


RUN pip install -r requirements.txt --no-cache-dir

RUN python manage.py collectstatic


CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ] 