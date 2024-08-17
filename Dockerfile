# Образ с системными зависимостями
FROM python:3.12-slim AS base-image

RUN mkdir /opt/proxy_mock
WORKDIR /opt/proxy_mock

RUN apt-get update && apt-get install -y git gcc gpp build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN python -m ensurepip --upgrade
RUN python -m pip install --upgrade pip setuptools wheel

# Ставим python-зависимости
FROM base-image AS build-image

RUN pip install poetry==1.8.2

RUN mkdir -p /www/proxy_mock/
WORKDIR /www/proxy_mock/
COPY pyproject.toml poetry.lock ./

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    poetry install --no-root

# Используем python из venv по умолчанию
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/var/www/proxy_mock

# Образ с приложением
FROM build-image

WORKDIR /var/www/proxy_mock
COPY . .

ARG CMD_ARG=""
ENV CMD_ARG=${CMD_ARG}

CMD ${CMD_ARG}
