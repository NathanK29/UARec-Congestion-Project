from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.runWebScrape, name="runWebScrape"),
    ]
