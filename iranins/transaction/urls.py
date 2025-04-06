from django.urls import path
from transaction.views import ChargeBalance, UserTransactions


urlpatterns = [
    path('balance/charge/', ChargeBalance.as_view(), name='charge-balance'),
    path('<int:pk>/all/', UserTransactions.as_view(), name='user-transactions'),
]