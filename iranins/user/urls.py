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

    path('profile/users/<int:pk>/insureds/add/', UserInsuredAdd.as_view(), name='user-insured-add'),
    path('profile/users/<int:user_pk>/insureds/<int:insured_pk>/delete/', UserInsuredDelete.as_view(), name='user-insured-delete'),
    path('profile/users/<int:user_pk>/insureds/<int:insured_pk>/edit/', UserInsuredEdit.as_view(), name='user-insured-edit'),
    path('profile/users/<int:pk>/insureds/', UserInsureds.as_view(), name='user-insureds'),

    path('profile/users/<int:user_pk>/insureds/<int:insured_pk>/insurances/add', InsuredInsuranceAdd.as_view(), name='insured-insurance-add'),
    path('profile/users/<int:user_pk>/insureds/<int:insured_pk>/insurances/<int:insurance_pk>/delete/', InsuredInsuranceDelete.as_view(), name='insured-insurance-delete'),
    path('profile/users/<int:user_pk>/insureds/<int:insured_pk>/insurances/<int:insurance_pk>/edit/', InsuredInsuranceEdit.as_view(), name='insured-insurance-edit'),
    path('profile/users/<int:user_pk>/insureds/<int:insured_pk>/insurances/', InsuredInsurance.as_view(), name='insured-insurance'),

    path('profile/users/<int:user_pk>/insureds/<int:insured_pk>/insurances/<int:insurance_pk>/installment/<int:installment_pk>/pay/',InstallmentPay.as_view(), name='installment-pay'),

    path('profile/', ProfileDashboard.as_view(), name='profile-dashboard'),

    path('logout/', ProfileLogout.as_view(), name='profile-logout'),
    path('error/', ErrorPage.as_view(), name='error-page'),
]
