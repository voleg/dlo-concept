ARG PYTHON_BASE=python:3.11-alpine

FROM $PYTHON_BASE AS builder

COPY --from=ghcr.io/astral-sh/uv:0.4.18 /uv /bin/uv
WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH" \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.11
COPY pyproject.toml uv.lock /code/
RUN uv sync
COPY . /code/
RUN python manage.py collectstatic --noinput

# run stage
FROM $PYTHON_BASE
COPY --from=builder /code/.venv/ /code/.venv
COPY --from=builder /code/static/ /code/static
ENV PATH="/code/.venv/bin:$PATH"

# set command/entrypoint, adapt to fit your needs
COPY . /code
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
SHELL ["/bin/sh", "-c"]
CMD python manage.py migrate; \
		python manage.py loaddata demo_init.json; \
		pytest; python manage.py runserver 0.0.0.0:8000
