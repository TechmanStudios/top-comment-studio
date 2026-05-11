FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    TOP_COMMENT_STUDIO_DATA_DIR=/data/local \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN uv sync --frozen --no-dev
RUN mkdir -p /data/local

EXPOSE 8000

CMD ["sh", "-c", "uvicorn top_comment_studio.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
