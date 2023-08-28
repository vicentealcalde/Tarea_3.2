FROM python:3.11-alpine as dev
WORKDIR /app
RUN pip install flask Flask-Alembic Flask-SQLAlchemy psycopg2-binary

FROM python:3.11-alpine as build
WORKDIR /build
COPY . /build/
RUN pip install build && \
    python -m build --wheel

FROM python:3.11-alpine as prod
RUN pip install -U pip
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
WORKDIR /home/appuser
COPY --chown=appuser:appgroup --from=build /build/dist/books-1.0.0-py3-none-any.whl /tmp/
RUN pip install --user /tmp/books-1.0.0-py3-none-any.whl gunicorn && \
    rm /tmp/books-1.0.0-py3-none-any.whl
ENV PATH="/home/appuser/.local/bin:${PATH}"
CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0", "books:create_app" ]
