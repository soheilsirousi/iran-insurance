from django.urls import path
from user.views import *


urlpatterns = [
    path('login/', UserLogin.as_view(), name='user-login'),
    path('send-otp/', SendOTP.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),

    path('profile/edit/', ProfileEdit.as_view(), name='profile-edit'),
    path('profile/users/add/', ProfileCreateUser.as_view(), name='profile-create-user'),
    path('profile/users/', ProfileUsers.as_view(), name='profile-users'),
    path('profile/users/<int:pk>/delete/', ProfileUserDelete.as_view(), name='profile-user-delete'),
    path('profile/users/<int:pk>/edit/', ProfileUserRetreive.as_view(), name='profile-user-retrieve'),
    path('profile/users/<int:pk>/insureds/', UserInsureds.as_view(), name='user-indureds'),
    path('profile/', ProfileDashboard.as_view(), name='profile-dashboard'),

    path('logout/', ProfileLogout.as_view(), name='profile-logout'),
    path('error/', ErrorPage.as_view(), name='error-page'),
]
