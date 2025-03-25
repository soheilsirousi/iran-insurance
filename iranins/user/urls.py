from django.urls import path
from user.views import *


urlpatterns = [
    path('login/', UserLogin.as_view(), name='user-login'),
    path('send-otp/', SendOTP.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
    path('profile/', ProfileDashboard.as_view(), name='profile-dashboard'),
]
