FROM python:latest
WORKDIR /code
COPY ./pyproject.toml ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev --no-root
COPY . .
