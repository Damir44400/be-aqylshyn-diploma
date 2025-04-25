FROM python:3.11

WORKDIR /app

RUN apt-get update && pip install poetry

COPY pyproject.toml poetry.lock ./


RUN pip install --upgrade pip poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root


COPY . .


RUN chmod +x start.sh

EXPOSE 8000

CMD ["bash", "start.sh"]