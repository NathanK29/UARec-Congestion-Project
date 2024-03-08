from django.urls import path, include
from . import views

urlpatterns = [
    path('run', views.runWebScrape, name="runWebScrape"),
    ]
