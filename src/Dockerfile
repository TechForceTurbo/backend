FROM python:3.11

RUN pip install poetry

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi && \
    poetry add gunicorn