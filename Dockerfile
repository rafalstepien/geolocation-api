FROM alpine:3.16.2 as alpine-base

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.15 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ENV ENV_FILE=/app/env/local.env

FROM alpine-base as builder-base

RUN apk update && \
    apk add --no-cache gcc libffi-dev musl-dev postgresql-dev python3-dev build-base python3 nginx && \
    ln -sf python3 /usr/bin/python && \
    python3 -m ensurepip && \
    pip3 install "poetry==$POETRY_VERSION"

COPY . /app

RUN poetry config virtualenvs.create false && \
    poetry install

CMD uvicorn geolocation_api.main:app --host 0.0.0.0 --port $PORT
