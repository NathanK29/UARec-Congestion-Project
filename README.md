# Running the Django API App

Ensure you are running Python 3.10.11 and have installed Redis and MySQL server on your system.

To run the Django API app, you must have three terminals opened (Or simply use the Dockerfiles to build an image to run the application).

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

### Running with Docker

Make sure Docker is running:

```bash
sudo systemctl start docker    (If you're using an EC2 instance)
docker-compose up --build
```
