from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView

from django_tables2 import LazyPaginator, SingleTableView

from .models import MoneyTransfer
from .tables import MoneyTransferTable, MoneyTransferedTable
from .forms import MoneyTransferDetailForm, MoneyTransferUpdateForm

# Create your views here.
class MoneyTransferListView(LoginRequiredMixin, SingleTableView):
    
    model = MoneyTransfer
    table_class = MoneyTransferTable
    template_name = 'money_transfer/money_transfer.html'
        
    paginator_class = LazyPaginator
    table_pagination = {'per_page': 10}
    queryset = MoneyTransfer.objects.filter(
        is_transfered=False
    )
    
    
class MoneyTransferedListView(LoginRequiredMixin, SingleTableView):
    
    model = MoneyTransfer
    table_class = MoneyTransferedTable
    template_name = 'money_transfer/money_transfer.html'
        
    paginator_class = LazyPaginator
    table_pagination = {'per_page': 10}
    queryset = MoneyTransfer.objects.filter(
        is_transfered=True
    )
    
    
class MoneyTransferDetailView(LoginRequiredMixin, UpdateView):
    
    model = MoneyTransfer
    template_name = 'money_transfer/money_transfer_detail.html'
    form_class = MoneyTransferUpdateForm
    
    def get(self, request, *args, **kwargs):
        self.money_transfer = self.get_object()
        
        if not self.money_transfer.is_transfered:
            return super().get(request, *args, **kwargs)
        return redirect('all-money-transfer')
    
    def get_success_url(self):
        return reverse('all-money-transfer')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial = {
            'trade_partner': self.money_transfer.trade_partner,
            'loan': self.money_transfer.loan,
            'employee': self.money_transfer.employee,
            'branch': self.money_transfer.branch
        }
        context['form_detail'] = MoneyTransferDetailForm(
            instance=self.money_transfer,
            initial=initial
        )
        context['form'] = MoneyTransferUpdateForm(
            instance=self.money_transfer,
        )
        return context
