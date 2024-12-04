FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /FastAPIExample

COPY . /FastAPIExample

RUN uv sync --frozen

CMD uv run uvicorn main:app --reload --workers 4 --port 5000 --host 0.0.0.0