from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView, \
    TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm, formset_factory
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from django_tables2 import LazyPaginator, SingleTableView

from django.core import serializers

from client.models import Client, Job, Spouse, ClientSpend

from .forms import (LoanConsultationForm, LoanConsultationDetailForm, LoanApplicationConclusionForm, LoanForm,
                    LoanApplicationForm, SocialAnalysisForm, SocialAnalysisReadForm, LoanApplicationConclusionConfirmForm)
from .tables import LoanConsultationTable, LoanApplicationTable, LoanApplicationConfirmTable, LoanTable
from .models import (LoanApplication, LoanProduct, LoanConsultation, Loan,
                     LoanInfo, LoanInfoChoices,
                     LoanApplicationConfirmHistory,
                     LoanApllicationConfirmEmployees, LoanAcceptanceStatus,
                     LoanInitialPaymentValue)
from .utlis import is_form_fields_is_empty

from employee_account.models import Employee, PositionHistory
from client.models import ClientSpend

from client.forms import (ClientForm, JobForm, SalaryForm, SpouseForm,
                          GuarantorForm, PassportForm, DependentForm,
                          ClientCommercialForm, SearchClientForm)
from trade_partner.forms import (ProductDetailForm, BaseProductDetailFormSet)
from deposits.forms import DepositForm


class CreateLoanConsultationView(LoginRequiredMixin, CreateView):
    form_class = LoanConsultationForm
    template_name = 'loan_system/loan-consultation.html'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.employee = get_object_or_404(Employee,
                                                   pk=self.request.user.pk)
        self.object = form.save()
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
        context['info'] = LoanInfo.objects.filter(
            name=LoanInfoChoices.CONSULT_INFO
        ).first()
        return context


class LoanConsultationListView(LoginRequiredMixin, SingleTableView):
    model = LoanConsultation
    table_class = LoanConsultationTable
    template_name = 'loan_system/loan-consultation-list.html'

    paginator_class = LazyPaginator
    table_pagination = {'per_page': 10}

    def get_queryset(self):
        return LoanConsultation.objects.filter(
            employee__id=self.request.user.id
        )


class CreateLoanApplicationView(LoginRequiredMixin, CreateView):
    model = LoanApplication
    form_class = LoanApplicationForm
    template_name = 'loan_system/loan-application.html'

    def form_valid(self, form):
        context = self.get_context_data()
        client_form = context['client_form']
        job_form = context['job_form']
        commercial_form = context['commercial_form']
        spouse_form = context['spouse_form']
        guarantor_form = context['guarantor_form']

        salary_form = context['salary_form']

        client_passport_form = context['client_passport_form']
        spouse_passport_form = context['spouse_passport_form']
        guarantor_passport_form = context['guarantor_passport_form']

        dependent_form = context['dependent_form']

        product_details_form = context['product_details_form']

        if all(context[f].is_valid() for f in context if isinstance(context[f], ModelForm)):
            is_spouse_fields_not_empty = is_form_fields_is_empty(
                spouse_passport_form, 'spouse')
            is_guarantor_fields_not_empty = is_form_fields_is_empty(
                guarantor_passport_form, 'guarantor')
            is_job_fields_not_empty = is_form_fields_is_empty(
                job_form, 'job'
            )

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

            if is_job_fields_not_empty:
                job = job_form.save(commit=False)
                job.client = client
                job.save()
            else:
                commercial = commercial_form.save(commit=False)
                commercial.client = client
                commercial.save()

            salary = salary_form.save(commit=False)
            salary.client = client
            salary.save()

            self.loan_application = form.save(commit=False)
            self.loan_application.client = client
            self.loan_application.branch = self.request.user.office_branch
            self.loan_application.employee = self.request.user
            self.loan_application.save()

            for product_detail_form in product_details_form:
                product_detail = product_detail_form.save(commit=False)
                product_detail.loan_application = self.loan_application
                product_detail.save()

            return redirect(reverse('loan-application-detail',
                                    kwargs={'pk': self.loan_application.pk}))

        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):

        path = self.request.path_info.split('/')

        context = super(CreateLoanApplicationView, self).get_context_data(**kwargs)
        context['client_id'] = None

        if len(path) >= 5:
            client_id = path[-2]
            client = Client.objects.filter(pk=client_id).first()
            if client is not None:
                context['client_id'] = client_id

        return self.get_all_forms(context)

    def get_all_forms(self, context):
        if context['client_id'] is not None:
            client = Client.objects.get(pk=context['client_id'])
            job = client.job.first()
            commercial = client.client_commercial.first()
            salary = client.client_salary.first()

            try:
                spouse = client.spouse
                spouse_passport = spouse.passport
            except Spouse.DoesNotExist:
                spouse = None
                spouse_passport = None

            guarantor = client.guarantor

            client_passport = client.passport
            guarantor_passport = guarantor.passport

            dependent = client.dependent.first()

            context['kind_of_work'] = client.kind_of_work

        else:
            client = None
            job = None
            commercial = None
            salary = None
            guarantor = None
            spouse = None
            spouse_passport = None
            client_passport = None
            guarantor_passport = None
            dependent = None

        loan_initial_payment_values = LoanInitialPaymentValue.objects.all()
        context['loan_initial_payment_values'] = serializers.serialize('json', loan_initial_payment_values)

        context['client_form'] = ClientForm(self.request.POST or None,
                                            prefix='client', instance=client)
        context['job_form'] = JobForm(self.request.POST or None, prefix='job', instance=job)
        context['commercial_form'] = ClientCommercialForm(
            self.request.POST or None, instance=commercial)

        context['salary_form'] = SalaryForm(self.request.POST or None, prefix='salary', instance=salary)
        context['spouse_form'] = SpouseForm(self.request.POST or None,
                                            prefix='spouse', instance=spouse)
        context['guarantor_form'] = GuarantorForm(self.request.POST or None,
                                                  prefix='guarantor', instance=guarantor)

        context['client_passport_form'] = PassportForm(
            self.request.POST or None, prefix='client', instance=client_passport)
        context['spouse_passport_form'] = PassportForm(
            self.request.POST or None, prefix='spouse', instance=spouse_passport)
        context['guarantor_passport_form'] = PassportForm(
            self.request.POST or None, prefix='guarantor', instance=guarantor_passport)

        context['dependent_form'] = DependentForm(self.request.POST or None, instance=dependent)

        context['loan_products'] = LoanProduct.objects.filter(is_active=True)
        ProductDetailFormSet = formset_factory(ProductDetailForm,
                                               formset=BaseProductDetailFormSet)

        context['product_details_form'] = ProductDetailFormSet(
            self.request.POST or None)

        context['form'] = LoanApplicationForm(self.request.POST or None)

        return context


class LoanApplicationListView(LoginRequiredMixin, SingleTableView):
    model = LoanApplication
    table_class = LoanApplicationTable
    template_name = 'loan_system/loan-application-list.html'

    paginator_class = LazyPaginator
    table_pagination = {'per_page': 10}

    def get_queryset(self):
        return LoanApplication.objects.filter(
            employee__id=self.request.user.id
        )


class LoanApplicationDetailView(LoginRequiredMixin, DetailView):
    model = LoanApplication
    template_name = 'loan_system/loan-application-detail.html'
    context_object_name = 'application'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        loan_application = self.get_object()
        dependet = loan_application.client.dependent.first()

        if hasattr(loan_application.client, 'job'):
            client_job = loan_application.client.job.first()
            context['job_form'] = JobForm(instance=client_job)

        if hasattr(loan_application.client, 'commercial_form'):
            client_commercial = loan_application.client.client_commercial.first()
            context['commercial_form'] = ClientCommercialForm(
                instance=client_commercial)

        if hasattr(loan_application.client, 'spouse'):
            context['spouse_form'] = SpouseForm(
                instance=loan_application.client.spouse,
                prefix='spouse')
            context['spouse_passport_form'] = PassportForm(
                instance=loan_application.client.spouse.passport,
                prefix='spouse')

        if hasattr(loan_application.client, 'guarantor'):
            context['guarantor_form'] = GuarantorForm(
                instance=loan_application.client.guarantor,
                prefix='guarantor')
            context['guarantor_passport_form'] = PassportForm(
                instance=loan_application.client.guarantor.passport,
                prefix='guarantor')

        if hasattr(loan_application, 'social_analysis'):

            form = SocialAnalysisReadForm(
                instance=loan_application.social_analysis)

            initial_data = {
                'full_name': loan_application.client,
                'age': loan_application.client.get_age,
                'is_married': loan_application.client.get_is_married_display(),
                'education': loan_application.client.get_education_status_display(),
                'is_judged': loan_application.client.get_is_criminal_record_display(),
            }

            if hasattr(loan_application.client, 'dependet'):
                initial_data.update(
                    {
                        'minor_children_amount': dependet.children_under_18,
                        'adult_children_amount': dependet.children_over_18,
                    }
                )

            if hasattr(loan_application.client, 'commercial_form'):
                initial_data.update(
                    {
                        'is_for_hire': _('Нет'),
                        'type_of_commercial_activity': client_commercial.organization_information,
                    }
                )

            if hasattr(loan_application.client, 'job'):
                initial_data.update(
                    {
                        'is_for_hire': _('Да'),
                        'type_of_commercial_activity': _(
                            'Нет комерческой деятельности'),
                        'duration_work_at_current_place': client_job.get_work_period,
                        'duration_work_at_previus_place': client_job.working_period_previous_job,
                        'duration_work_at_penultimate_place': client_job.working_period_penultimate_job,
                    }
                )

            form.initial.update(
                initial_data
            )

            context['social_analysis_form'] = form

        context['client_passport_form'] = PassportForm(
            instance=loan_application.client.passport, prefix='client')
        context['client_form'] = ClientForm(instance=loan_application.client,
                                            prefix='client')
        context['client_form'] = ClientForm(instance=loan_application.client, prefix='client')
        context['dependent_form'] = DependentForm(instance=dependet)
        context['salary_form'] = SalaryForm(
            instance=loan_application.client.client_salary.first())
        context['form'] = LoanApplicationForm(instance=loan_application)
        ProductDetailFormSet = formset_factory(ProductDetailForm,
                                               formset=BaseProductDetailFormSet)

        context['product_details_form'] = ProductDetailFormSet(
            initial=loan_application.product_buy.all().values())

        if loan_application.give_out_status == CreditAcceptanceStatus.with_bail:
            position = PositionHistory.objects.filter(
                employee=loan_application.employee,
                is_current=True
            ).first()

        context['client_spend'] = ClientSpend.objects.all()
        context['limit'] = position.position.limits.filter(
                end_date__gte=loan_application.updated_date,
                start_date__lte = loan_application.updated_date
            ).first()
        
        ProductDetailFormSet = formset_factory(ProductDetailForm,
                                               formset=BaseProductDetailFormSet)

        context['product_details_form'] = ProductDetailFormSet(initial=loan_application.product_buy.all().values())
        
        if loan_application.give_out_status == LoanAcceptanceStatus.with_bail:
            context.update(
                loan_application.loan_application_confirms_check()
            )
            
        context['info'] = LoanInfo.objects.filter(
            name=LoanInfoChoices.ADVICE
        ).first()
        
        return context


class CreateLoanApplicationSocialAnalysisView(LoginRequiredMixin, CreateView):
    form_class = SocialAnalysisForm
    template_name = 'loan_system/loan-application-social-analysis.html'

    def get(self, request, *args, **kwargs):

        self.loan_application = get_object_or_404(LoanApplication,
                                                  pk=self.kwargs['pk'])

        if hasattr(self.loan_application, 'social_analysis'):
            return self.get_success_url(self.loan_application.id)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = SocialAnalysisForm()
        initial_data = {
            'full_name': self.loan_application.client,
            'age': self.loan_application.client.get_age,
            'is_married': self.loan_application.client.get_is_married_display(),
            'education': self.loan_application.client.get_education_status_display(),
            'is_judged': self.loan_application.client.get_is_criminal_record_display(),
        }

        if hasattr(self.loan_application.client, 'dependet'):
            dependet = self.loan_application.client.dependet.all().first()
            initial_data.update(
                {
                    'minor_children_amount': dependet.children_under_18,
                    'adult_children_amount': dependet.children_over_18,
                }
            )

        if not hasattr(self.loan_application.client, 'client_commercial'):
            client_commercial = self.loan_application.client.client_commercial.all().first()
            initial_data.update(
                {
                    'is_for_hire': _('Нет'),
                    'type_of_commercial_activity': client_commercial.organization_information,
                }
            )

        if hasattr(self.loan_application.client, 'job'):
            job = self.loan_application.client.job.first()
            if job:
                initial_data.update(
                    {
                        'is_for_hire': _('Да'),
                        'type_of_commercial_activity': _(
                            'Нет комерческой деятельности'),
                        'duration_work_at_current_place': job.get_work_period,
                        'duration_work_at_previus_place': job.working_period_previous_job,
                        'duration_work_at_penultimate_place': job.working_period_penultimate_job,
                    }
                )

        form.initial = initial_data

        context['form'] = form
        context['loan_application'] = self.loan_application
        return context

    def form_valid(self, form):
        form = form.save(commit=False)
        form.loan_application = get_object_or_404(LoanApplication,
                                                  pk=self.kwargs['pk'])
        form.save()
        return self.get_success_url(
            pk=form.loan_application.id
        )

    def get_success_url(self, pk):
        return redirect(reverse('loan-application-detail', kwargs={'pk': pk}))


class CreateLoanApplicationConclusionView(LoginRequiredMixin, UpdateView):
    model = LoanApplication
    form_class = LoanApplicationConclusionForm
    template_name = 'loan_system/loan-application-conclusion.html'

    def get(self, request, *args, **kwargs):
        self.loan_application = get_object_or_404(LoanApplication,
                                                  pk=self.kwargs['pk'])

        if hasattr(self.loan_application,
                   'social_analysis') and self.loan_application.give_out_status != 'not_accept':
            return self.get_success_url(
                pk=self.loan_application.id
            )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'loan_application': self.loan_application,
                'client_spend': ClientSpend.objects.all()
            }
        )
        return context

    def form_valid(self, form):
        form = form.save()
        position = PositionHistory.objects.filter(
            employee=form.employee,
            is_current=True
        ).first()
        
        position_limit = position.position.limits.filter(
                end_date__gte=form.updated_date,
                start_date__lte = form.updated_date
            ).first()

        if (position_limit.limit >= form.funding_amount) and form.give_out_status == LoanAcceptanceStatus.with_bail:
            confirms_list = []
            for confirm_employee in LoanApllicationConfirmEmployees.objects.filter(
                is_active=True
            ):
                confirms_list.append(
                    LoanApplicationConfirmHistory(
                        loan_application=form,
                        employee=confirm_employee,
                        is_confirm=True
                    )
                )
            LoanApplicationConfirmHistory.objects.bulk_create(
                confirms_list
            )
            form.is_accept = True
            form.save(
                update_fileds=('is_accept',)
            )
        return self.get_success_url(
            pk=form.id
        )

    def get_success_url(self, pk):
        return redirect(reverse('loan-application-detail', kwargs={'pk': pk}))


class LoanApplicationConfirmConclusionListView(LoginRequiredMixin,
                                               SingleTableView):
    model = LoanApplication
    table_class = LoanApplicationConfirmTable
    template_name = 'loan_system/loan-application-list.html'

    paginator_class = LazyPaginator
    table_pagination = {'per_page': 10}

    def get(self, request, *args, **kwargs):
        can_confirm_employees = LoanApllicationConfirmEmployees.objects.filter(
            is_active=True
        ).values_list('employee__pk', flat=True)
        if request.user.id in can_confirm_employees:
            return super().get(request, *args, **kwargs)
        return redirect('my-profile')

    def get_queryset(self):
        all_confirmed_loan_applications = LoanApplicationConfirmHistory.objects.filter(
            employee__employee__id=self.request.user.id
        ).values_list('loan_application', flat=True)
        return LoanApplication.objects.filter(
            is_accept=False,
            is_processing=True,
            give_out_status='bail'
        ).filter(
            ~Q(id__in=all_confirmed_loan_applications)
        )


class LoanApplicationConfirmedConclusionListView(
    LoanApplicationConfirmConclusionListView):
    table_class = LoanApplicationTable

    def get_queryset(self):
        all_confirmed_loan_applications = LoanApplicationConfirmHistory.objects.filter(
            employee__employee__id=self.request.user.id
        ).values_list('loan_application', flat=True)

        return LoanApplication.objects.filter(
            is_accept=True,
            is_processing=True,
            give_out_status='bail',
            id__in=all_confirmed_loan_applications
        )


class LoanApplicationConfirmConclusionDetailView(LoginRequiredMixin,
                                                 CreateView):
    model = LoanApplicationConfirmHistory
    template_name = 'loan_system/loan-application-detail.html'
    context_object_name = 'application'
    form_class = LoanApplicationConclusionConfirmForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        loan_application = get_object_or_404(LoanApplication,
                                             pk=self.kwargs['pk'])
        dependet = loan_application.client.dependet.first()

        if hasattr(loan_application.client, 'job'):
            client_job = loan_application.client.job.first()
            context['job_form'] = JobForm(instance=client_job)

        if hasattr(loan_application.client, 'commercial_form'):
            client_commercial = loan_application.client.client_commercial.first()
            context['commercial_form'] = ClientCommercialForm(
                instance=client_commercial)

        if hasattr(loan_application.client, 'spouse'):
            context['spouse_form'] = SpouseForm(
                instance=loan_application.client.spouse.first(),
                prefix='spouse')
            context['spouse_passport_form'] = PassportForm(
                instance=loan_application.client.spouse.passport,
                prefix='spouse')

        if hasattr(loan_application.client, 'guarantor'):
            context['guarantor_form'] = GuarantorForm(
                instance=loan_application.client.guarantor.first(),
                prefix='guarantor')
            context['guarantor_passport_form'] = PassportForm(
                instance=loan_application.client.guarantor.passport,
                prefix='guarantor')

        if hasattr(loan_application, 'social_analysis'):

            form = SocialAnalysisReadForm(
                instance=loan_application.social_analysis)

            initial_data = {
                'full_name': loan_application.client,
                'age': loan_application.client.get_age,
                'is_married': loan_application.client.get_is_married_display(),
                'education': loan_application.client.get_education_status_display(),
                'is_judged': loan_application.client.get_is_criminal_record_display(),
            }

            if hasattr(loan_application.client, 'dependet'):
                initial_data.update(
                    {
                        'minor_children_amount': dependet.children_under_18,
                        'adult_children_amount': dependet.children_over_18,
                    }
                )

            if hasattr(loan_application.client, 'commercial_form'):
                initial_data.update(
                    {
                        'is_for_hire': _('Нет'),
                        'type_of_commercial_activity': client_commercial.organization_information,
                    }
                )

            if hasattr(loan_application.client, 'job'):
                initial_data.update(
                    {
                        'is_for_hire': _('Да'),
                        'type_of_commercial_activity': _(
                            'Нет комерческой деятельности'),
                        'duration_work_at_current_place': client_job.get_work_period,
                        'duration_work_at_previus_place': client_job.working_period_previous_job,
                        'duration_work_at_penultimate_place': client_job.working_period_penultimate_job,
                    }
                )

            form.initial.update(
                initial_data
            )

            context['social_analysis_form'] = form

        context['client_passport_form'] = PassportForm(
            instance=loan_application.client.passport, prefix='client')
        context['client_form'] = ClientForm(instance=loan_application.client,
                                            prefix='client')
        context['dependent_form'] = DependentForm(instance=dependet)
        context['salary_form'] = SalaryForm(
            instance=loan_application.client.client_salary.first())
        context['form'] = LoanApplicationForm(instance=loan_application)

        ProductDetailFormSet = formset_factory(ProductDetailForm,
                                               formset=BaseProductDetailFormSet)

        context['product_details_form'] = ProductDetailFormSet(
            initial=loan_application.product_buy.all().values())

        if loan_application.give_out_status == CreditAcceptanceStatus.with_bail:
            context['client_spend'] = ClientSpend.objects.all()
            position = PositionHistory.objects.filter(
                employee=loan_application.employee,
                is_current=True
            ).first()
        context['limit'] = position.position.limits.filter(
                end_date__gte=loan_application.updated_date,
                start_date__lte = loan_application.updated_date
            ).first()
        
        ProductDetailFormSet = formset_factory(ProductDetailForm,
                                               formset=BaseProductDetailFormSet)

        context['product_details_form'] = ProductDetailFormSet(initial=loan_application.product_buy.all().values())
        
        if loan_application.give_out_status == LoanAcceptanceStatus.with_bail:
            context.update(
                loan_application.loan_application_confirms_check()
            )

        context[
            'loan_application_confirm_form'] = LoanApplicationConclusionConfirmForm(
            self.request.POST or None)

        return context

    def form_valid(self, form):
        form = form.save(commit=False)
        form.loan_application = get_object_or_404(LoanApplication,
                                                  pk=self.kwargs['pk'])
        form.employee = get_object_or_404(LoanApllicationConfirmEmployees,
                                          employee__pk=self.request.user.pk)
        form.save()
        return self.get_success_url(
            pk=form.loan_application.id
        )

    def get_success_url(self, pk):
        return redirect(reverse('loan-application-detail', kwargs={'pk': pk}))


class CreateLoanView(LoginRequiredMixin, DetailView):
    model = LoanApplication

    def get(self, request, *args, **kwargs):
        loan_application = LoanApplication.objects.get(
            pk=kwargs.get('pk')
        )
        if not hasattr(loan_application, 'loan') and loan_application.is_accept and \
            (loan_application.give_out_status == LoanAcceptanceStatus.with_bail):
            
            Loan.objects.create_loan(
                loan_application=loan_application,
                urgent_principal_debt=loan_application.total_cost_with_surcharge,
                rppu=0,
                rppu_percent=0,
                loan_purpose='Потребительский кредит',
                collateral='Залог описание',
                collateral_cost=20000,
                
                request=request
            )
            loan_application.is_registered = True
            loan_application.save(
                update_fields=['is_registered']
            )
        return redirect('my-profile')


class LoanListView(LoginRequiredMixin, SingleTableView):
    model = Loan
    table_class = LoanTable
    template_name = 'loan_system/loan-list.html'

    paginator_class = LazyPaginator
    table_pagination = {'per_page': 10}

    def get_queryset(self):
        return Loan.objects.filter(
            loan_application__employee__id=self.request.user.id
        )


class LoanDetailView(LoginRequiredMixin, DetailView):
    model = Loan
    template_name = 'loan_system/loan-detail.html'
    context_object_name = 'application'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        loan = self.get_object()
        loan_application = loan.loan_application

        dependet = loan_application.client.dependet.first()

        if hasattr(loan_application.client, 'job'):
            client_job = loan_application.client.job.first()
            context['job_form'] = JobForm(instance=client_job)

        if hasattr(loan_application.client, 'commercial_form'):
            client_commercial = loan_application.client.client_commercial.first()
            context['commercial_form'] = ClientCommercialForm(
                instance=client_commercial)

        if hasattr(loan_application.client, 'spouse'):
            context['spouse_form'] = SpouseForm(
                instance=loan_application.client.spouse.first(),
                prefix='spouse')
            context['spouse_passport_form'] = PassportForm(
                instance=loan_application.client.spouse.passport,
                prefix='spouse')

        if hasattr(loan_application.client, 'guarantor'):
            context['guarantor_form'] = GuarantorForm(
                instance=loan_application.client.guarantor.first(),
                prefix='guarantor')
            context['guarantor_passport_form'] = PassportForm(
                instance=loan_application.client.guarantor.passport,
                prefix='guarantor')

        if hasattr(loan_application, 'social_analysis'):

            form = SocialAnalysisReadForm(
                instance=loan_application.social_analysis)

            initial_data = {
                'full_name': loan_application.client,
                'age': loan_application.client.get_age,
                'is_married': loan_application.client.get_is_married_display(),
                'education': loan_application.client.get_education_status_display(),
                'is_judged': loan_application.client.get_is_criminal_record_display(),
            }

            if hasattr(loan_application.client, 'dependet'):
                initial_data.update(
                    {
                        'minor_children_amount': dependet.children_under_18,
                        'adult_children_amount': dependet.children_over_18,
                    }
                )

            if hasattr(loan_application.client, 'commercial_form'):
                initial_data.update(
                    {
                        'is_for_hire': _('Нет'),
                        'type_of_commercial_activity': client_commercial.organization_information,
                    }
                )

            if hasattr(loan_application.client, 'job'):
                initial_data.update(
                    {
                        'is_for_hire': _('Да'),
                        'type_of_commercial_activity': _(
                            'Нет комерческой деятельности'),
                        'duration_work_at_current_place': client_job.get_work_period,
                        'duration_work_at_previus_place': client_job.working_period_previous_job,
                        'duration_work_at_penultimate_place': client_job.working_period_penultimate_job,
                    }
                )

            form.initial.update(
                initial_data
            )

            context['social_analysis_form'] = form

        context['client_passport_form'] = PassportForm(
            instance=loan_application.client.passport, prefix='client')
        context['client_form'] = ClientForm(instance=loan_application.client,
                                            prefix='client')
        context['dependent_form'] = DependentForm(instance=dependet)
        context['salary_form'] = SalaryForm(
            instance=loan_application.client.client_salary.first())
        context['form'] = LoanApplicationForm(instance=loan_application)

        ProductDetailFormSet = formset_factory(ProductDetailForm,
                                               formset=BaseProductDetailFormSet)

        context['product_details_form'] = ProductDetailFormSet(
            initial=loan_application.product_buy.all().values())
        context['loan_form'] = LoanForm(instance=loan, prefix='loan')

        if loan_application.give_out_status == CreditAcceptanceStatus.with_bail:
          context['deposit_form'] = DepositForm(instance=loan.deposit_account, prefix='deposit')
          context['client_spend'] = ClientSpend.objects.all()
        
          context.update(
                loan_application.loan_application_confirms_check()
            )

        return context


class ClientExistView(LoginRequiredMixin, View):
    template_name = 'loan_system/client-exist.html'
    form_class = SearchClientForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):

        client_id = request.POST.get('pin')

        if client_id is None:
            return HttpResponseNotFound()

        form = self.form_class()

        return redirect('loan-application', pk=client_id)
