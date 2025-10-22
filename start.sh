# poetry run gunicorn --workers 4 app.asgi:application -k uvicorn_worker.UvicornWorker  --reload
poetry run python manage.py runserver