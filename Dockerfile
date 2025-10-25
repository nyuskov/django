# Use a alpine Python image
FROM python:3.13-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the application code
COPY . .
COPY /nginx/certificates /certificates
RUN rm -rf /nginx /start.sh

# Install dependencies
RUN apk update && apk upgrade && apk add libpq-dev && apk add build-base
RUN pip install poetry && poetry install --no-root

# Expose the port your app listens on
EXPOSE 8000

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the application when the container starts
CMD ["poetry", "run", "gunicorn", "--bind", "unix:/tmp/gunicorn.sock",\
     "--certfile", "/certificates/server.crt",\
     "--keyfile", "/certificates/server.key",\
     "--workers", "4", "app.asgi:application",\
     "-k", "uvicorn_worker.UvicornWorker"]



