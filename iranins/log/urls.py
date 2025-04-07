from django.urls import path
from .views import Logs


urlpatterns = [
    path('', Logs.as_view(), name='logs'),
]
