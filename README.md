# Running the Django API App

To run the Django API app, you must have three terminals opened. Also, ensure Redis is installed and running on your system.

### Terminal 1: Django App
Activate the virtual environment and run the Django development server:

```bash
. .\.venv\Scripts\activate
cd .\API\
python manage.py runserver
```

### Terminal 2: Celery
Activate the virtual environment and start the Celery worker:

```bash
. .\.venv\Scripts\activate
cd .\API\
celery -A API.celery worker --pool=solo -l info
```

### Terminal 3: Celery Beat
Activate the virtual environment and start the Celery Beat scheduler:

```bash
. .\.venv\Scripts\activate
cd .\API\
celery -A API beat --loglevel=info
```
