FROM python:3.10-slim

WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry
RUN poetry install --no-root --no-dev
COPY . .
CMD ["poetry", "run", "python", "main.py"]
