FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"

RUN poetry self update

WORKDIR /core_api

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi


COPY src/ ./src

COPY . .

CMD uvicorn src.main:app --host 0.0.0.0 --port 80 --proxy-headers --forwarded-allow-ips '*' --root-path $ROOT_PATH