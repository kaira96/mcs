from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Deposit
from .forms import DepositPayForm, DepositAccountSearchForm, DepositDetailForm
from .service import hide_owner_info

# Create your views here.
class DepositAccountPayView(LoginRequiredMixin, CreateView):
    
    form_class = DepositDetailForm
    template_name = 'deposits/deposit-pay.html'
    
    def post(self, request, *args, **kwargs):
        self.object = None
        if self.request.POST.get('deposit_account_number'):
            context = self.get_context_data(*args, **kwargs)
            return render(
                request=request,
                template_name='deposits/deposit-pay.html',
                context=context
            )
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['deposit_account_search_form'] = DepositAccountSearchForm()
                                
        if deposit_account_number := self.request.POST.get('deposit_account_number'):
                        
            deposit_account = Deposit.objects.filter(
                account_number=deposit_account_number
            ).first()
            
            if deposit_account:
                context['deposit_account_detail_form'] = DepositDetailForm(
                    instance=deposit_account,
                    initial = {
                        'client': deposit_account.client
                    }                    
                )
                context['form'] = DepositPayForm(
                    initial={'number':deposit_account.account_number}
                )
            else:
                context['deposit_account_search_form'] = DepositAccountSearchForm()
                context['deposit_message'] = _(f'Депозитный счёт {deposit_account_number} не найден.')
        
        if self.request.POST.get('top_up_amount'):
            context['deposit_pay_form'] = DepositPayForm(self.request.POST or None)
            
        return context    

    def form_valid(self, form):
        context = self.get_context_data()
        
        form = context['deposit_pay_form']
        
        if form.is_valid():
            if deposit_account_number := self.request.POST.get('deposit_number'):     
                deposit_account = Deposit.objects.filter(
                    account_number=deposit_account_number
                ).first()
                deposit_account.current_balance += form.cleaned_data['top_up_amount']
                deposit_account.save(request=self.request)
                context['deposit_account_search_form'] = DepositAccountSearchForm()
                context['deposit_message'] = _('Депозитный счёт пополнен.')
                return render(
                    request=self.request,
                    template_name='deposits/deposit-pay.html',
                    context=context
                )
            else:
                context['deposit_account_search_form'] = DepositAccountSearchForm()
                context['deposit_message'] = _(f'Депозитный счёт {deposit_account_number} не найден.')
                return render(
                    request=self.request,
                    template_name='deposits/deposit-pay.html',
                    context=context
                )
        else:
            context['deposit_account_search_form'] = DepositAccountSearchForm()
            context['deposit_message'] = form.errors
            return render(
                request=self.request,
                template_name='deposits/deposit-pay.html',
                context=context
            )
            
            
class DepositAccountCheckApiView(DetailView):
    
    model = Deposit
    template_name = 'deposits/deposit-check.html'
    
    def get(self, request, *args, **kwargs):
        if deposit_account_number := kwargs.get('pk'):
            deposit_account = Deposit.objects.filter(
                account_number=deposit_account_number
            ).first()
            if deposit_account:
                owner_info = hide_owner_info(
                        str(deposit_account.client).title().split()[:-1]
                    )
                return JsonResponse(
                    data={
                        'message':_('Депозитный счёт найден.'),
                        'owner_info': {
                            'first_name': owner_info[0],
                            'last_name': owner_info[1],
                        }
                    },
                    safe=False,
                    json_dumps_params={
                        'ensure_ascii': False
                    }
                )
            return JsonResponse(
                    data={
                        'message':_('Депозитный счёт не найден.')
                    },
                    safe=False,
                    json_dumps_params={
                        'ensure_ascii': False
                    }
                )
            