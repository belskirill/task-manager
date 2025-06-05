FROM python:3.11.9



# Установка системных зависимостей
RUN apt-get update && apt-get install -y curl build-essential libpq-dev && apt-get clean

# Установка poetry (официальный способ)
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /app
ENV PYTHONPATH=/app

COPY pyproject.toml poetry.lock* ./

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

CMD poetry run alembic upgrade head; poetry run python src/main.py