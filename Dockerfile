FROM python:3.9

WORKDIR /app

COPY . .
ENV PYTHONUNBUFFERED=1
RUN pip3 install -r requirements.txt
RUN python3 manage.py test

CMD ["uwsgi", "--http", "0.0.0.0:8000", "--module", "django_project.wsgi"]