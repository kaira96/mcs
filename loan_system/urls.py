from django.urls import path, include

from .views import (CreateLoanConsultationView, LoanConsultationDetailView,
                    LoanConsultationListView,
                    CreateLoanApplicationView, LoanApplicationDetailView,
                    LoanApplicationListView,
                    CreateLoanApplicationSocialAnalysisView,
                    CreateLoanApplicationConclusionView,
                    LoanApplicationConfirmConclusionListView,
                    LoanApplicationConfirmConclusionDetailView,
                    LoanApplicationConfirmedConclusionListView, CreateLoanView,
                    LoanListView, LoanDetailView, ClientExistView)

urlpatterns = [
    path('', include('trade_partner.urls')),
    path('', include('client.urls')),
    path(
        'loan-detail/<int:pk>/',
        LoanDetailView.as_view(),
        name='loan-detail'
    ),
    path(
        'create-loan/<int:pk>/',
        CreateLoanView.as_view(),
        name='create-loan'
    ),
    path(
        'all-loan/',
        LoanListView.as_view(),
        name='all-loan'
    ),
    path(
        'loan-application-confirm-conclusion/<int:pk>/',
        LoanApplicationConfirmConclusionDetailView.as_view(),
        name='loan-application-confirm-detail'
    ),
    path(
        'all-loan-application-confirmed-conclusion/',
        LoanApplicationConfirmedConclusionListView.as_view(),
        name='all-loan-application-confirmed-conclusion'),
    path(
        'all-loan-application-confirm-conclusion/',
        LoanApplicationConfirmConclusionListView.as_view(),
        name='all-loan-application-confirm-conclusion'),
    path(
        'loan-application-conclusion/<int:pk>/',
         CreateLoanApplicationConclusionView.as_view(),
        name='loan-application-conclusion'
    ),
    path(
        'loan-application-social-analysis/<int:pk>/',
        CreateLoanApplicationSocialAnalysisView.as_view(),
        name='loan-application-social-analysis'
    ),
    path(
        'loan-application-detail/<int:pk>/',
        LoanApplicationDetailView.as_view(),
        name='loan-application-detail'
    ),
    path(
        'all-application/',
        LoanApplicationListView.as_view(),
        name='all-application'),
    path(
        'loan-application/',
        CreateLoanApplicationView.as_view(),
        name='loan-application-without-initial'
    ),
    path(
        'loan-application/<int:pk>/',
        CreateLoanApplicationView.as_view(),
        name='loan-application'
    ),
    path(
        'client/',
        ClientExistView.as_view(),
        name='client-exist'
    ),
    path(
        'consultation-detail/<int:pk>/',
        LoanConsultationDetailView.as_view(),
        name='loan-consultation-detail'
    ),
    path(
        'all-consultation/',
        LoanConsultationListView.as_view(),
        name='all-consultation'
    ),
    path(
        'consultation/',
        CreateLoanConsultationView.as_view(),
        name='loan-consultation'
    ),
]
