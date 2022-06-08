release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn rapid_basket.wsgi --log-file - 