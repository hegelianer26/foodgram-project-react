FROM python:3.7-slim

WORKDIR /app

COPY ./ /app


RUN pip install -r requirements.txt --no-cache-dir


RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --no-input
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ] 