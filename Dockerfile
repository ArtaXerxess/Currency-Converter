# syntax=docker/dockerfile:1

# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.12.0
FROM python:${PYTHON_VERSION}-slim as base


ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app


# https://docs.docker.com/go/dockerfile-user-best-practices/

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

USER appuser

COPY . .

EXPOSE 80

CMD uvicorn 'src.main:app' --host=0.0.0.0 --port=80
