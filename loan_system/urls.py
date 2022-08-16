from django.urls import path, include

from .views import (CreateLoanConsultationView, LoanConsultationDetailView, LoanConsultationListView, 
                    CreateLoanApplicationView, LoanApplicationDetailView, LoanApplicationListView)

urlpatterns = [
    path('', include('trade_partner.urls')),
    
    path('application-detail/<int:pk>/', LoanApplicationDetailView.as_view(), name='loan-application-detail'),
    path('all-application/', LoanApplicationListView.as_view(), name='all-application'),
    path('loan-application/', CreateLoanApplicationView.as_view(), name='loan-application'),
    
    path('consultation-detail/<int:pk>/', LoanConsultationDetailView.as_view(), name='loan-consultation-detail'),
    path('all-consultation/', LoanConsultationListView.as_view(), name='all-consultation'),
    path('consultation/', CreateLoanConsultationView.as_view(), name='loan-consultation'),
]
