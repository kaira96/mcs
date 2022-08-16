from django.urls import path, re_path

from .views import DepositAccountPayView, DepositAccountCheckApiView

urlpatterns = [
    path('pay/', DepositAccountPayView.as_view(), name='deposit-pay'),
    path('check/<int:pk>/', DepositAccountCheckApiView.as_view(), name='deposit-account-check-api')
]
