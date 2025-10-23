rm -f /tmp/gunicorn.sock
poetry run gunicorn --bind unix:/tmp/gunicorn.sock --workers 4 app.asgi:application -k uvicorn_worker.UvicornWorker  --reload
# poetry run python manage.py runserver