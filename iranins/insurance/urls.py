from django.urls import path
from .views import *


urlpatterns = [
    path('<int:pk>/reminder/', InsuranceReminder.as_view(), name='insurance-reminder'),

]