from django.urls import path
from .views import my_api_view
urlpatterns = [
    path('api/data/', my_api_view),  # Route for the API
]
