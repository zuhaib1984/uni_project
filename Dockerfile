FROM python:3.9.18

WORKDIR /app

COPY ./ ./
 
CMD python manage.py