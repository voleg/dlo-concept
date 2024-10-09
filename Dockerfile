FROM python:3.11-alpine
COPY --from=ghcr.io/astral-sh/uv:0.4.18 /uv /bin/uv
WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH" \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.11

COPY pyproject.toml uv.lock /code/

RUN uv sync --frozen
ADD . /code
CMD 'sh'
