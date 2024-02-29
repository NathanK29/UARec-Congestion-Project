from django.shortcuts import render
from .tasks import scrape_webcams
from django.http import HttpResponse

# Create your views here.
def runWebScrape(request):
    """
    A view that triggers the scrape_webcams Celery task asynchronously and returns an HTTP response immediately.
    """
    try:
        scrape_webcams.delay()
        message = "Scrape webcams task has been initiated."
    except Exception as e:
        # Log the error or handle it appropriately
        message = f"Failed to initiate scrape webcams task: {e}"
    return HttpResponse(message)


# def schedule_task(request):
   