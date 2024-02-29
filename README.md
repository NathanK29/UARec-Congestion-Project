To run the Django API app, you need three terminals opened.
Also, ensure Redis is installed and running on your system.

Terminal 1. Django App
  . .\.venv\Scripts\activate
  cd .\API\
  python manage.py runserver
Terminal 2. Celery
  . .\.venv\Scripts\activate
  cd .\API\
  celery -A API.celery worker --pool=solo -l info
Terminal 3. Celery Beat
  . .\.venv\Scripts\activate
  cd .\API\
  celery -A API beat --loglevel=info
