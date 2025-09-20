FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt


COPY .flake8 .
COPY . .

ENV SECRET_KEY='django-insecure-i)+xv5p+0b$!q)ihq+0dweq+lus-x*fh3b5awm+_k%)vev!hb*'
ENV CELERY_BROKER_URL='redis://localhost:6379'
ENV CELERY_BACKEND='redis://localhost:6379'


RUN mkdir -p /app/media
RUN mkdir -p /app/static
RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

EXPOSE 8080

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8080"]
