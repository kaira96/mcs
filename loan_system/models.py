from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q

from dateutil.relativedelta import relativedelta

from client.models import BOOL_CHOICES

from deposits.models import Deposit

from accounting_balance.models import AccountTransactionTemplates, AccountTransactionTemplate

from money_transfer.models import MoneyTransfer

from .service import generate_repayment_dates

from accounting_balance.models import (AccountTransactionTemplates, Transaction, AccountTransactionTemplate,
                                       Balance)

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
    

class LoanAcceptanceStatus(models.TextChoices): 
    with_bail = 'bail', _('Выдача с залогом ')
    rejection = 'rejection', _('Сформировать отказ')
    not_accept = 'not_accept', _('Решение не принято')
    
    
class RelevanceOfTheProfession(models.TextChoices):
    HIGH = 'H', _('Высоко востребованная')
    MIDDLE = 'M', _('Средне востребованная')
    LOW = 'L', _('Низко востребованная')
    NOT_REVELANCE = 'N', _('Не востребованная')
    
    
class ClientLoansHistory(models.TextChoices):
    POSITIVE = 'P', _('Положительная')
    NEGATIVE = 'N', _('Негативная')


class ClientBehavior(models.TextChoices):
    POLITE = 'P', _('Вежливое')
    NEUTRAL = 'N', _('Нейтральное')
    RUDE = 'R', _('Грубое')
    
    
class AccrualStatusChoices(models.TextChoices):
    ACCRUALS = 'A', _('Начисления')
    NOT_ACCRUALS = 'NA', _('Не начисления')
    JUDICIAL = 'J', _('Судебный')
    
    
class LoanInfoChoices(models.TextChoices):
    ADVICE = 'A', _('Рекомендации системы')
    CONSULT_INFO = 'CI', _('Информация для консультации')

    
PROCESS_CHOICES = ((True, _('Обработанно')), (False, _('В стадии обработки')))


REVIEW_CHOICES = ((True, _('Рассмотренно')), (False, _('В стадии рассмотрения')))


class LoanApplication(models.Model):
    client = models.ForeignKey(
        'client.Client',
        on_delete=models.PROTECT,
        verbose_name=_('Клиент'),
    )
    employee = models.ForeignKey(
        'employee_account.Employee',
        on_delete=models.PROTECT,
        verbose_name=_('Сотрудник'),
        related_name='my_loan_applications'
    )
    branch = models.ForeignKey(
        'company_structure.OfficeBranch',
        on_delete=models.PROTECT,
        verbose_name=_('Филиал')
    )
    loan_product = models.ForeignKey(
        'LoanProduct',
        on_delete=models.PROTECT,
        verbose_name=_('Кредитный продукт'),
    )
    funding_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Сумма финансирования'),
        help_text=_('Coм'),
        validators=[MinValueValidator(3000), MaxValueValidator(200_000)],
    )
    funding_period = models.PositiveSmallIntegerField(
        verbose_name=_('Срок финансирования'),
        help_text=_('В месяцах'),
        validators=[MinValueValidator(0)],
        choices=(
            (24, 24),
            (21, 21),
            (18, 18),
            (15, 15),
            (12, 12),
            (9, 9),
            (6, 6),
            (3, 3)
        )
    )
    first_instalment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Первый взнос'),
        help_text=_('Сом'),
        validators=[MinValueValidator(0)],
    )
    bank_surcharge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Сумма наценки банка'),
        help_text=_('Сом')
    )
    total_cost_with_surcharge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Общая сумма с наценкой'),
        help_text=_('Сом'),
        validators=[MinValueValidator(0)],
    )
    monthly_payment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Ежемесячный платеж'),
        help_text=_('Сом'),
        validators=[MinValueValidator(0)],
    )
    start_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Дата выдачи кредита')
    )
    end_date = models.DateField(
        verbose_name=_('Дата окончания кредита')
    )
    is_accept = models.BooleanField(
        verbose_name=_('Решение кредитного комитета (Выдать кредит)'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    is_processing = models.BooleanField(
        verbose_name=_('Статус обработки'),
        choices=REVIEW_CHOICES,
        default=REVIEW_CHOICES[1][0]
    )
    is_registered = models.BooleanField(
        verbose_name=_('Кредит оформлен'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    give_out_status = models.CharField(
        verbose_name=_('Решение сотрудника'),
        choices=LoanAcceptanceStatus.choices,
        default=LoanAcceptanceStatus.not_accept,
        max_length=20,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания записи')
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи')
    )

        
    def get_absolute_url(self):
        return reverse('loan-application-detail', kwargs={'pk': self.id})
        
    def repayment_schedule(self):
        return generate_repayment_dates(self=self)
        
    def effect_percentage(self):
        return round(100 * (self.bank_surcharge / self.funding_amount), ndigits=2)
    
    def kib_check(self):
        KIBAnalysis.objects.create(
            loan_application=self
        )
    
    def tunduk_check(self):
        TundukAnalysis.objects.create(
            loan_application=self
        )
    
    # def get_loan_amount2words(self, number):
    #         return num2words(
    #             number=number,
    #             lang=get_language(),
    #             to='currency',
    #             currency='KGS'
    #         ) 
    
    def first_instalment_percentage(self):
        return round(100 * (self.first_instalment / self.funding_amount), ndigits=2)

    def loan_application_confirms_check(self) -> dict:
        result = {}
        
        result['confirms'] = LoanApplicationConfirmHistory.objects.filter(
                loan_application__id=self.id
            )
        result['not_confirms'] = LoanApllicationConfirmEmployees.objects.filter(
                ~Q(employee__id__in=[confirm.employee.employee.id for confirm in result['confirms']])
                )

        if result['not_confirms'].count() == 0:
            result['loan_application_is_confirm'] = all([employee.is_confirm for employee in result['confirms']])
        
        return result

    def save(self, *args, **kwargs):
        if self.id is None:
            self.start_date = timezone.now()
            self.branch = self.employee.office_branch
            repayment_schedule = self.repayment_schedule()
            month_payment = repayment_schedule[1].month_payment
            self.funding_amount = self.funding_amount - self.first_instalment

            # calc bank surcharge
            self.total_cost_with_surcharge = sum([payment.month_payment for payment in repayment_schedule])
            # calc total bank surcharge
            self.bank_surcharge = self.total_cost_with_surcharge - self.funding_amount
            # calc per month payment
            self.monthly_payment = month_payment
            # Find end date
            self.end_date = timezone.now().today() + relativedelta(months=self.funding_period)
                # If its credit was create first time here create loan payment graph
            super().save(*args, **kwargs)
            self.kib_check()
            self.tunduk_check()
        super().save(*args, **kwargs)

    def loan_product_percent(self):
        return str(self.loan_product.get_percent())
    
    loan_product_percent.short_description = _('% ставка')
    
    def __str__(self):
        return _('Заявка №') + str(self.id)
    
    class Meta:
        verbose_name = _('Заявка на кредит')
        verbose_name_plural = _('Заявка на кредиты')
        ordering = ('-created_date',)
    
    
class LoanConsultation(models.Model):
    loan_product = models.ForeignKey(
        'LoanProduct',
        on_delete=models.PROTECT,
        verbose_name=_('Кредитный продукт'),
    )
    funding_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Сумма финансирования'),
        help_text=_('Coм'),
        validators=[MinValueValidator(0)],
    )
    funding_period = models.PositiveSmallIntegerField(
        verbose_name=_('Срок финансирования'),
        help_text=_('В месяцах'),
        validators=[MinValueValidator(0)],
    )
    first_instalment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Первый взнос'),
        help_text=_('Сом'),
        validators=[MinValueValidator(0)],
    )
    monthly_payment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Ежемесячный платеж'),
        help_text=_('Сом'),
        validators=[MinValueValidator(0)],
    )
    bank_surcharge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Сумма наценки банка'),
        help_text=_('Сом')
    )
    total_cost_with_surcharge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Общая сумма с наценкой'),
        help_text=_('Сом'),
        validators=[MinValueValidator(0)],
    )
    is_re_financing = models.BooleanField(
        verbose_name=_('Повторное финансирование'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    is_employer = models.BooleanField(
        verbose_name=_('Сотрудник нашего банка'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    is_gurantor = models.BooleanField(
        verbose_name=_('Есть поручитель'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[0][0]
    )
    start_date = models.DateField(
        verbose_name=_('Дата выдачи кредита')
    )
    employee = models.ForeignKey(
        'employee_account.Employee',
        on_delete=models.PROTECT,
        verbose_name=_('Сотрудник'),
        related_name='my_loan_consultations'
    )
    end_date = models.DateField(
        verbose_name=_('Дата окончания кредита')
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания записи')
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи')
    )
    
    def get_absolute_url(self):
        return reverse('loan-consultation-detail', kwargs={'pk': self.id})
    
    def repayment_schedule(self):
        return generate_repayment_dates(self=self)
    
    def effect_percentage(self):
        return round(100 * (self.bank_surcharge / self.funding_amount), ndigits=2)

    def first_instalment_percentage(self):
        return round(100 * (self.first_instalment / self.funding_amount), ndigits=2)
    
    def loan_product_percent(self):
        return str(self.loan_product.get_percent())
    
    loan_product_percent.short_description = _('% ставка')
    
    def __str__(self):
        return _('Консультация №') + str(self.id)
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.start_date = timezone.now()
            repayment_schedule = self.repayment_schedule()
            month_payment = repayment_schedule[1].month_payment
            self.funding_amount = self.funding_amount - self.first_instalment

            # calc bank surcharge
            self.total_cost_with_surcharge = sum([payment.month_payment for payment in repayment_schedule])
            # calc total bank surcharge
            self.bank_surcharge = self.total_cost_with_surcharge - self.funding_amount
            # calc per month payment
            self.monthly_payment = month_payment
            # Find end date
            self.end_date = timezone.now().today() + relativedelta(months=self.funding_period)
            super().save(*args, **kwargs)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = _('Консультация на кредит')
        verbose_name_plural = _('Консультация на кредиты')
        ordering = ('-created_date',)


class LoanProduct(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Имя')
    )
    percent = models.DecimalField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(1)],
        max_digits=3,
        decimal_places=2,
        verbose_name=_('% ставка')
    )
    is_active = models.BooleanField(
        verbose_name=_('Активный'),
        default=True,
    )
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата начала')
    )
    end_date = models.DateTimeField(
        default=timezone.datetime(
            year=2999,
            month=12,
            day=31,
            hour=12,
        ),
        verbose_name=_('Дата конца')
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания записи')
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи')
    )

    def __str__(self):
        return str(self.name)
    
    def get_percent(self):
        return f'{int(self.percent * 100)} %'
    
    get_percent.short_description = _('% ставка')
    
    class Meta:
        verbose_name = _('Кредитный продукт')
        verbose_name_plural = _('Кредитные продукты')
        ordering = ('-created_date',)
    
    
class LoanDocument(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_('Название документа')
    )
    loan_product = models.ForeignKey(
        LoanProduct,
        verbose_name=_("Кредитный продукт"),
        on_delete=models.PROTECT,
        related_name="documents"
    )
    start_date = models.DateTimeField(
        auto_now_add=True
    )
    end_date = models.DateTimeField(
        default=timezone.datetime(
            year=2999,
            month=12,
            day=31,
            hour=12,
        )
    )
    document = models.FileField(
        verbose_name=_('Загрузите файл формата doc or docx'),
        upload_to='documents/%Y/%m/%d'
    )
    is_active = models.BooleanField(
        default=True
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = _('Документ')
        verbose_name_plural = _('Документы')
        ordering = ('-created_date',)
        
        
class SocialAnalysis(models.Model): 
    loan_application = models.OneToOneField(
        LoanApplication,
        verbose_name=_('Заявка на кредит'),
        on_delete=models.PROTECT,
        related_name='social_analysis'
    )
    profession_relevance = models.CharField(
        verbose_name=_('Востребованность профессии'),
        max_length=1,
        choices=RelevanceOfTheProfession.choices,
        default=RelevanceOfTheProfession.MIDDLE
        )
    is_match = models.BooleanField(
        verbose_name=_('Слова соответсвуют с информацией по КИБу'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[0][0]
    )
    client_loans_history = models.CharField(
        verbose_name=_('Кредитная история клиента'),
        max_length=20,
        choices=ClientLoansHistory.choices,
        default=ClientLoansHistory.POSITIVE
    )
    own_house_address = models.CharField(
        verbose_name=_('Собственное жилье клиента распологается'),
        max_length=50,
    )
    has_a_car = models.BooleanField(
        verbose_name=_('Есть автомобиль у клиента'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    сlient_behavior = models.CharField(
        verbose_name=_('Поведение клиента во время анкетирования было'),
        max_length=1,
        choices=ClientBehavior.choices,
        default=ClientBehavior.POLITE
    )
    is_swear = models.BooleanField(
        verbose_name=_('Клиент использует ненормативную лексику'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    is_sharia_type_of_activity = models.BooleanField(
        verbose_name=_('Вид деятельности соответсвует шариату'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    is_positive = models.BooleanField(
        verbose_name=_('Социальный анализ положителен'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('Социальный анализ')
        verbose_name_plural = _('Социальные анализы')
        ordering = ('-created_date',)
        
    def __str__(self):
        return str(self.loan_application)
    
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.loan_application.is_processing = True
            self.loan_application.save()
            super().save(*args, **kwargs)
        super().save(*args, **kwargs)        
        
        
class KIBAnalysis(models.Model):
    loan_application = models.OneToOneField(
        LoanApplication,
        verbose_name=_('Заявка на кредит'),
        related_name='kib_analysis',
        on_delete=models.PROTECT
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __str__(self):
        return str(self.loan_application)
    
    class Meta:
        verbose_name = _('КИБ')
        verbose_name_plural = _('КИБ')
        ordering = ('-created_date',)
        
        
class TundukAnalysis(models.Model):
    loan_application = models.OneToOneField(
        LoanApplication,
        verbose_name=_('Заявка на кредит'),
        related_name='tunduk_analysis',
        on_delete=models.PROTECT
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __str__(self):
        return str(self.loan_application)
    
    class Meta:
        verbose_name = _('Тундук')
        verbose_name_plural = _('Тундук')
        ordering = ('-created_date',)        


class LoanApllicationConfirmEmployees(models.Model):
    employee = models.OneToOneField(
        'employee_account.Employee',
        verbose_name=_('Сотрудник ответственный за акцепт выдачи кредита'),
        related_name='loan_application_confirm_employee',
        on_delete=models.PROTECT,
    )
    is_active = models.BooleanField(
        verbose_name=_('Активный'),
        default=True
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __str__(self):
        return str(self.employee)
    
    class Meta:
        verbose_name = _('Сотрудник ответственный за акцепт выдачи кредита')
        verbose_name_plural = _('Сотрудники ответственные за акцепт выдачи кредита')
        ordering = ('-created_date',)


class LoanApplicationConfirmHistory(models.Model):
    loan_application = models.ForeignKey(
        LoanApplication,
        verbose_name=_('Заявка на кредит'),
        related_name='loan_application_confirm',
        on_delete=models.PROTECT
    )
    employee = models.ForeignKey(
        LoanApllicationConfirmEmployees,
        verbose_name=_('Сотрудник ответственный за акцепт выдачи кредита'),
        related_name='loan_application_confirm_employee',
        on_delete=models.PROTECT
    )
    is_confirm = models.BooleanField(
        verbose_name=_('Выдать кредит'),
        choices=BOOL_CHOICES,
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        application_confirm_info = self.loan_application.loan_application_confirms_check()
        
        if application_confirm_info.get('loan_application_is_confirm'):
            self.loan_application.is_accept = True
            self.loan_application.save(
                update_fields=['is_accept']
            )

    
    def __str__(self):
        return f'{self.employee} -> {self.loan_application}'
    
    class Meta:
        verbose_name = _('Акцепт на кредитную заявку')
        verbose_name_plural = _('Акцепты на кредитные заявки')
        ordering = ('-created_date',)
        unique_together = ('loan_application', 'employee')


class LoanManager(models.Manager):
    
    def create_loan(self, request, **kwargs):
        new_loan = self.model(**kwargs)
        new_loan.save(request=request)
        return new_loan
    
    
class Loan(models.Model):
    objects = LoanManager() 
    
    loan_application = models.OneToOneField(
        LoanApplication,
        verbose_name=_('Заявка на кредит'),
        related_name='loan',
        on_delete=models.PROTECT
    )
    deposit_account = models.ForeignKey(
        'deposits.Deposit',
        verbose_name=_('Депозитный счёт'),
        related_name='deposit_account',
        on_delete=models.PROTECT
    )
    balance_account = models.ForeignKey(
        'accounting_balance.Account',
        verbose_name=_('Балансовый счёт'),
        related_name='balance_accounts',
        on_delete=models.PROTECT
    )
    urgent_principal_debt = models.DecimalField(
        verbose_name=_('Срочный основной долг'),
        validators=[MinValueValidator(0)],
        max_digits=12,
        decimal_places=2,
    )
    overdue_principal_debt = models.DecimalField(
        verbose_name=_('Просроченный основной долг'),
        validators=[MinValueValidator(0)],
        max_digits=12,
        decimal_places=2,
        default=0
    )
    accrued_interest = models.DecimalField(
        verbose_name=_('Начисленные проценты'),
        validators=[MinValueValidator(0)],
        max_digits=12,
        decimal_places=2,
        default=0
    )
    classification = models.PositiveSmallIntegerField(
        verbose_name=_('Классификация кредита'),
        validators=[MinValueValidator(0),
                    MaxValueValidator(6)],
        default=6
    )
    classification_percent = models.DecimalField(
        verbose_name=_('Классификация кредита в %'),
        validators=[MinValueValidator(0),
                    MaxValueValidator(1)],
        max_digits=3,
        decimal_places=1,
        default=0
    )
    rppu = models.DecimalField(
        verbose_name=_('РППУ'),
        validators=[MinValueValidator(0)],
        max_digits=12,
        decimal_places=2,
        default=0
    )
    rppu_percent = models.DecimalField(
        verbose_name=_('РППУ %'),
        validators=[MinValueValidator(0),
                    MaxValueValidator(1)],
        max_digits=3,
        decimal_places=1,
        default=0
    )
    loan_purpose = models.CharField(
        max_length=50,
        verbose_name=_('Назначение кредита')
    )
    collateral = models.CharField(
        max_length=150,
        verbose_name=_('Залоговое обеспечение')
    )
    collateral_cost = models.CharField(
        max_length=150,
        verbose_name=_('Стоимость залогового обеспечения'),
    )
    is_restructuring = models.BooleanField(
        verbose_name=_('Кредит реструктуризирован'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    restructuring_date = models.DateTimeField(
        verbose_name=_('Дата реструктуризации кредита'),
    )
    restructuring_count = models.PositiveIntegerField(
        verbose_name=_('Кол-во реструктуризаций'),
        default=0
    )
    discount = models.DecimalField(
        verbose_name=_('Дисконт'),
        validators=[MinValueValidator(0)],
        max_digits=12,
        decimal_places=2,
        default=0
    )
    discount_percent = models.DecimalField(
        verbose_name=_('Дисконт %'),
        validators=[MinValueValidator(0),
                    MaxValueValidator(1)],
        max_digits=3,
        decimal_places=1,
        default=0
    )
    overdue_days_quantity = models.PositiveSmallIntegerField(
        verbose_name=_('Кол-во просроченных дней'),
        default=0
    )
    total_overdue_days_quantity = models.PositiveSmallIntegerField(
        verbose_name=_('Итого кол-во просроченных дней'),
        default=0
    )
    is_overdue = models.BooleanField(
        verbose_name=_('просрочено'),
        default=False
    )
    accrual_status = models.CharField(
        verbose_name=_('статус начисления'),
        max_length=20,
        default=AccrualStatusChoices.ACCRUALS,
        choices=AccrualStatusChoices.choices
    )
    accrual_status_date = models.DateField(
        verbose_name=_('Дата статуса'),
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev_accrual_status = self.accrual_status
        self.prev_restructuring_status = self.is_restructuring
        self.first_save = False
        
    
    def save(self, request, *args, **kwargs):
        
        if self.id is None:
            self.first_save = True
            self.accrual_status_date = timezone.now().today()
            self.restructuring_date = timezone.now()
            
            deposit_account = Deposit.objects.get_or_create(
                client=self.loan_application.client,
                defaults={
                    'balance_account': get_object_or_404(
                        AccountTransactionTemplate, 
                        transaction_template=AccountTransactionTemplates.repayment_of_financing_by_the_borrower
                        ).to_account,
                    'employee': self.loan_application.employee,
                    'branch': self.loan_application.branch
                },
            )
            
            self.deposit_account = deposit_account[0]
            self.balance_account = get_object_or_404(
                        AccountTransactionTemplate, 
                        transaction_template=AccountTransactionTemplates.recognition_of_financing
                        ).from_account
            
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

            if x_forwarded_for:
                ipaddress = x_forwarded_for.split(',')[-1].strip()
            else:
                ipaddress = request.META.get('REMOTE_ADDR')
            
            transaction_first = get_object_or_404(
                AccountTransactionTemplate, 
                transaction_template=AccountTransactionTemplates.payment_for_trade_partner
                )
            transaction_second = get_object_or_404(
                AccountTransactionTemplate, 
                transaction_template=AccountTransactionTemplates.acceptance_of_goods_for_other_property
                )
            transaction_third = get_object_or_404(
                AccountTransactionTemplate, 
                transaction_template=AccountTransactionTemplates.recognition_of_financing
                )
            transaction_firth = get_object_or_404(
                AccountTransactionTemplate, 
                transaction_template=AccountTransactionTemplates.accrual_income_for_all_period
                )
            
            description_template = f' -> {self.loan_application} | {self.loan_application.branch} | {timezone.now()}'
                
            transaction_list = (
                Transaction(
                        ip_address=ipaddress,
                        debit=transaction_first.from_account,
                        credit=transaction_first.to_account,
                        amount=self.loan_application.funding_amount,
                        description=f'{transaction_first.get_transaction_template_display()}' + description_template,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    ),
                Transaction(
                        ip_address=ipaddress,
                        debit=transaction_second.from_account,
                        credit=transaction_second.to_account,
                        amount=self.loan_application.funding_amount,
                        description=f'{transaction_second.get_transaction_template_display()}' + description_template,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    ),
                Transaction(
                        ip_address=ipaddress,
                        debit=transaction_third.from_account,
                        credit=transaction_third.to_account,
                        amount=self.loan_application.funding_amount,
                        description=f'{transaction_third.get_transaction_template_display()}' + description_template,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    ),
                Transaction(
                        ip_address=ipaddress,
                        debit=transaction_firth.from_account,
                        credit=transaction_firth.to_account,
                        amount=self.loan_application.bank_surcharge,
                        description=f'{transaction_firth.get_transaction_template_display()}' + description_template,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    )
            )

            balance_list = (
                    Balance(
                        account=transaction_first.from_account,
                        debit_amount=self.loan_application.funding_amount,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    ),
                    Balance(
                        account=transaction_first.to_account,
                        credit_amount=self.loan_application.funding_amount,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    ),
                    
                    Balance(
                        account=transaction_second.from_account,
                        debit_amount=self.loan_application.funding_amount,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    ),
                    Balance(
                        account=transaction_second.to_account,
                        credit_amount=self.loan_application.funding_amount,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    ),
                    Balance(
                        account=transaction_third.from_account,
                        debit_amount=self.loan_application.funding_amount,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    ),
                    Balance(
                        account=transaction_third.to_account,
                        credit_amount=self.loan_application.funding_amount,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    ),
                    Balance(
                        account=transaction_firth.from_account,
                        debit_amount=self.loan_application.bank_surcharge,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    ),
                    Balance(
                        account=transaction_firth.to_account,
                        credit_amount=self.loan_application.bank_surcharge,
                        branch=self.loan_application.branch,
                        employee=self.loan_application.employee
                    )
                )
            
            Transaction.objects.bulk_create(
                transaction_list
            )
            Balance.objects.bulk_create(
                balance_list
            )
        
        if (self.prev_restructuring_status != self.is_restructuring) and self.is_restructuring:
            self.restructuring_date = timezone.now()
        
        if self.prev_accrual_status != self.accrual_status:
            self.accrual_status_date = timezone.now()
            
        super().save(*args, **kwargs)
        
        if self.first_save:
            products_list = self.loan_application.product_buy.all()
            
            MoneyTransfer.objects.bulk_create(
                [
                    MoneyTransfer(
                        trade_partner=product.trade_partner,
                        loan=self,
                        employee=self.loan_application.employee,
                        branch=self.loan_application.branch,
                        transfer_amount=product.price
                    ) for product in products_list
                ]
            )
            self.first_save = False
    
    def __str__(self):
        return _('Кредит № ') + str(self.id)
    
    class Meta:
        verbose_name = _('Кредит')
        verbose_name_plural = _('Кредиты')
        ordering = ('-created_date',)
        unique_together = ('loan_application', 'deposit_account')


class LoanInitialPaymentValue(models.Model):
    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Сумма приобретаемого товара (от этой суммы будет \
            считаться сумма первоначального взноса)'),
        validators=[MinValueValidator(0)]
    )
    initial_payment_percent = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('% Первоначального взноса от указанной суммы приобретаемого товара'),
        validators=[MinValueValidator(0),
                    MaxValueValidator(1)],
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __str__(self):
        return f'{self.total_cost} -> {self.initial_payment_percent}'
    
    def get_percent(self):
        return f'{int(self.initial_payment_percent * 100)} %'
    
    get_percent.short_description = _('% ставка')
    
    class Meta:
        verbose_name = _('Плановая сумма для первоначального взноса')
        verbose_name_plural = _('Плановые суммы для первоначального взноса')
        ordering = ('-created_date',)
        unique_together = ('total_cost', 'initial_payment_percent')


class LoanLimitAmount(models.Model):
    position = models.OneToOneField(
        'company_structure.Position',
        on_delete=models.PROTECT,
        verbose_name=_('Должность'),
        related_name='loan_limit'
    )
    limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Лимит суммы финансирования на данную позицию'),
        validators=[MinValueValidator(0)]
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_limit = self.limit
    
    def __str__(self):
        return f'{self.position} -> {self.limit}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.previous_limit != self.limit:
            loan_limit = LoanLimitAmountHistory.objects.filter(
                is_current=True, 
                position=self.position).first()
            
            if loan_limit:
                loan_limit.end_date = timezone.now()
                loan_limit.is_current = False
                loan_limit.save()
                
            LoanLimitAmountHistory(
                    position=self.position,
                    limit=self.limit
                ).save()
        
    class Meta:
        verbose_name = _('Лимит финансирования без акцепта кредитного коммитета')
        verbose_name_plural = _('Лимиты финансирования без акцепта кредитного коммитета')
        ordering = ('-created_date',)


class LoanLimitAmountHistory(models.Model):
    position = models.ForeignKey(
        'company_structure.Position',
        on_delete=models.PROTECT,
        verbose_name=_('Должность'),
        related_name='limits'
    )
    limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Лимит суммы финансирования на данную позицию'),
        validators=[MinValueValidator(0)]
    )
    is_current = models.BooleanField(
        default=True,
        verbose_name=_('Актуальный лимит?'),
        help_text=_('format: required, max_length=255')
    )
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата начала лимита'),
        help_text=_('format: required')
    )
    end_date = models.DateTimeField(
        default=timezone.datetime(
            year=2999,
            month=12,
            day=31,
            hour=12,
        ),
        verbose_name=_('Дата окончания этого лимита'),
        help_text=_('format: required')
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __str__(self):
        return f'{self.position} -> {self.limit}'
    
    class Meta:
        verbose_name = _('История лимита финансирования без акцепта кредитного коммитета')
        verbose_name_plural = _('История лимитов финансирования без акцепта кредитного коммитета')
        ordering = ('-created_date',)
    
    
class LoanInfo(models.Model):
    name = models.CharField(
        verbose_name=_('Название информации'),
        max_length=10,
        choices=LoanInfoChoices.choices,
        unique=True
    )
    text = RichTextUploadingField(
        verbose_name=_('Текст информации'),
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = _('Информация')
        verbose_name_plural = _('Информации')
        ordering = ('-created_date',)
        