FROM python:3.13-slim-bullseye

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . /app
RUN groupadd www && useradd -g www -d /opt/www -m www && chown -R www:www /app
USER www
WORKDIR /app
RUN uv sync --locked --no-cache

CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80"]
