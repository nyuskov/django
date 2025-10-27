sudo rm -rf /tmp/gunicorn.sock
poetry run gunicorn --bind unix:/tmp/gunicorn.sock --certfile ~/certificates/server.crt --keyfile ~/certificates/server.key --workers 1 app.asgi:application -k uvicorn_worker.UvicornWorker  --reload
# poetry run python manage.py runserver