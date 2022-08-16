from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm, formset_factory

from django_tables2 import LazyPaginator, SingleTableView

from .forms import LoanConsultationForm, LoanConsultation, LoanConsultationDetailForm, LoanApplicationForm
from .tables import LoanConsultationTable, LoanApplicationTable
from .models import LoanApplication, LoanProduct
from .utlis import is_form_fields_is_empty

from employee_account.models import Employee

from client.forms import (ClientForm, JobForm, SalaryForm, SpouseForm,
                          GuarantorForm, PassportForm, DependentForm, ClientCommercialForm)

from trade_partner.forms import (ProductDetailForm, BaseProductDetailFormSet)


import logging


logger = logging.getLogger('main')

# Create your views here.
class CreateLoanConsultationView(LoginRequiredMixin, CreateView):
    
    form_class = LoanConsultationForm
    template_name = 'loan_system/loan-consultation.html'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.employee = get_object_or_404(Employee, pk=self.request.user.pk)
        self.object = form.save()
        logger.info('Test')
        return super().form_valid(form)
    
    
class LoanConsultationDetailView(LoginRequiredMixin, DetailView):
    
    model = LoanConsultation
    template_name = 'loan_system/loan-consultation-detail.html'
    context_object_name = 'consultation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'form': LoanConsultationDetailForm(instance=self.get_object())
            }
        )
        return context
   

class LoanConsultationListView(LoginRequiredMixin, SingleTableView):
    
    model = LoanConsultation
    table_class = LoanConsultationTable
    template_name = 'loan_system/loan-consultation-list.html'
        
    paginator_class = LazyPaginator
    table_pagination = {'per_page': 10}
   
   
class CreateLoanApplicationView(LoginRequiredMixin, CreateView):
    model = LoanApplication
    form_class = LoanApplicationForm
    template_name = 'loan_system/loan-application.html'
        
    def form_valid(self, form):
        context = self.get_context_data()
        client_form = context['client_form']
        job_form = context['job_form']

        spouse_form = context['spouse_form']
        guarantor_form = context['guarantor_form']

        salary_form = context['salary_form']

        client_passport_form = context['client_passport_form']
        spouse_passport_form = context['spouse_passport_form']
        guarantor_passport_form = context['guarantor_passport_form']

        dependent_form = context['dependent_form']

        product_details_form = context['product_details_form']
                
        if all(context[f].is_valid() for f in context if isinstance(context[f], ModelForm)):

            is_spouse_fields_not_empty = is_form_fields_is_empty(spouse_passport_form, 'spouse')
            is_guarantor_fields_not_empty = is_form_fields_is_empty(guarantor_passport_form, 'guarantor')

            client_passport = client_passport_form.save()

            client = client_form.save(commit=False)
            client.passport = client_passport
            client.save()

            dependent_form.save(commit=False)
            dependent_form.instance.client = client
            dependent_form.save()

            if is_guarantor_fields_not_empty:
                guarantor_passport = guarantor_passport_form.save()
                guarantor = guarantor_form.save(commit=False)
                guarantor.passport = guarantor_passport
                guarantor.client = client
                guarantor.save()

            if is_spouse_fields_not_empty:
                spouse_passport = spouse_passport_form.save()
                spouse_form.save(commit=False)
                spouse_form.instance.client = client
                spouse_form.instance.passport = spouse_passport
                spouse_form.save()

            job = job_form.save(commit=False)
            job.client = client
            job.save()

            salary = salary_form.save(commit=False)
            salary.client = client
            salary.save()

            self.loan_application = form.save(commit=False)
            self.loan_application.client = client
            self.loan_application.employee = self.request.user
            self.loan_application.save()

            for product_detail_form in product_details_form:
                product_detail = product_detail_form.save(commit=False)
                product_detail.loan_application = self.loan_application
                product_detail.save()

            return redirect(self.get_success_url())

        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreateLoanApplicationView, self).get_context_data(**kwargs)
        context = self.get_all_forms(context)

        return context

    def get_all_forms(self, context):
        context['loan_products'] = LoanProduct.objects.filter(is_active=True)

        context['client_form'] = ClientForm(self.request.POST or None, prefix='client')
        context['job_form'] = JobForm(self.request.POST or None)
        context['salary_form'] = SalaryForm(self.request.POST or None)
        context['commercial_form'] = ClientCommercialForm(self.request.POST or None)

        context['spouse_form'] = SpouseForm(self.request.POST or None, prefix='spouse')
        context['guarantor_form'] = GuarantorForm(self.request.POST or None, prefix='guarantor')

        context['client_passport_form'] = PassportForm(self.request.POST or None, prefix='client')
        context['spouse_passport_form'] = PassportForm(self.request.POST or None, prefix='spouse')
        context['guarantor_passport_form'] = PassportForm(self.request.POST or None, prefix='guarantor')

        context['dependent_form'] = DependentForm(self.request.POST or None)

        ProductDetailFormSet = formset_factory(ProductDetailForm,
                                               formset=BaseProductDetailFormSet)

        context['product_details_form'] = ProductDetailFormSet(self.request.POST or None)

        context['form'] = LoanApplicationForm(self.request.POST or None)

        return context
    

class LoanApplicationListView(LoginRequiredMixin, SingleTableView):
    
    model = LoanApplication
    table_class = LoanApplicationTable
    template_name = 'loan_system/loan-application-list.html'
        
    paginator_class = LazyPaginator
    table_pagination = {'per_page': 10}
    

class LoanApplicationDetailView(LoginRequiredMixin, DetailView):
    
    model = LoanApplication
    template_name = 'loan_system/loan-application-detail.html'
    context_object_name = 'application'
    
    def get_context_data(self, **kwargs):
        
        loan_application = self.get_object()
        
        context = super().get_context_data(**kwargs)
        context['client_form'] = ClientForm(instance=loan_application.client, prefix='client')
        context['salary_form'] = SalaryForm(instance=loan_application.client.client_salary.all()[:1][0])
        
        if hasattr(loan_application.client, 'job'):
            context['job_form'] = JobForm(instance=loan_application.client.job.all()[:1][0])
        if hasattr(loan_application.client, 'commercial_form'):
            context['commercial_form'] = ClientCommercialForm(instance=loan_application.client.commercial_form)
            # context['commercial_form'] = ClientCommercialForm(instance=loan_application.client.commercial_form.all()[:1][0])
            
        context['client_passport_form'] = PassportForm(instance=loan_application.client.passport, prefix='client')
        
        if hasattr(loan_application.client, 'spouse'):
            context['spouse_form'] = SpouseForm(instance=loan_application.client.spouse.all()[:1][0], prefix='spouse')
            context['spouse_passport_form'] = PassportForm(instance=loan_application.client.spouse.passport, prefix='spouse')
        if hasattr(loan_application.client, 'guarantor'):
            context['guarantor_form'] = GuarantorForm(instance=loan_application.client.guarantor.all()[:1][0], prefix='guarantor') 
            context['guarantor_passport_form'] = PassportForm(instance=loan_application.client.guarantor.passport, prefix='guarantor')

        context['dependent_form'] = DependentForm(instance=loan_application.client.dependet.all()[:1][0])
        context['form'] = LoanApplicationForm(instance=loan_application)
        
        ProductDetailFormSet = formset_factory(ProductDetailForm,
                                               formset=BaseProductDetailFormSet)

        context['product_details_form'] = ProductDetailFormSet(initial=loan_application.product_buy.all().values())
                
        return context
    
  
