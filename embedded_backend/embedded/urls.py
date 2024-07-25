from django.urls import path
from .views import rfid_view

urlpatterns = [
    path('rfid', rfid_view, name='rfid_view'),
]
