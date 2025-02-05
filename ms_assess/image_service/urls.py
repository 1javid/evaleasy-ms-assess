# image_service/urls.py
from django.urls import path
from .views import submit_assessment

urlpatterns = [
    path('submit-assessment/', submit_assessment, name='submit_assessment'),
]
