from django.urls import path
from .views import MoneyTransferListView, MoneyTransferDetailView, MoneyTransferedListView

urlpatterns = [
    path('detail/<int:pk>/', MoneyTransferDetailView.as_view(), name='money-transfer-detail'),
    path('all-transfered/', MoneyTransferedListView.as_view(), name='all-money-transfered'),
    path('all/', MoneyTransferListView.as_view(), name='all-money-transfer'),
]
