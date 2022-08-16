from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.urls import reverse

from dateutil.relativedelta import relativedelta

from client.models import BOOL_CHOICES

from .service import generate_repayment_dates

# Create your models here.
    

class CreditAcceptanceStatus(models.TextChoices):
    with_bail = 'bail', _('Выдача с залогом ')
    without_collateral = 'collateral', _('Выдача без залога')
    rejection = 'rejection', _('Сформировать отказ')
    under_review = 'review', _('В стадии рассмотрения')
    

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
        related_name='loans'
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
    acceptance_status = models.CharField(
        verbose_name='Статус принятия',
        choices=CreditAcceptanceStatus.choices,
        default=CreditAcceptanceStatus.under_review,
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('loan-application-detail', kwargs={'pk': self.id})
        
    def repayment_schedule(self):
        return generate_repayment_dates(self=self)
        
    def effect_percentage(self):
        return round(100 * (self.bank_surcharge / self.funding_amount), ndigits=2)
    
    
    # def get_loan_amount2words(self, number):
    #         return num2words(
    #             number=number,
    #             lang=get_language(),
    #             to='currency',
    #             currency='KGS'
    #         ) 
    
    def first_instalment_percentage(self):
        return round(100 * (self.first_instalment / self.funding_amount), ndigits=2)

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
                # If its credit was create first time here create loan payment graph        
            super().save(*args, **kwargs)
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
        related_name='loan_consultation'
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
    
    client = models.ForeignKey(
        'client.Client',
        verbose_name=_('Клиент'),
        on_delete=models.PROTECT,
        related_name='social_analysis'
    )
    loan_application = models.OneToOneField(
        LoanApplication,
        verbose_name=_('Кредит'),
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
        default=True
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
        default=True
    )
    сlient_behavior = models.CharField(
        verbose_name=_('Поведение клиента во время анкетирования было'),
        max_length=1,
        choices=ClientBehavior.choices,
        default=ClientBehavior.POLITE
    )
    is_swear = models.BooleanField(
        verbose_name=_('Клиент использует ненормативную лексику'),
        default=False
    )
    is_sharia_type_of_activity = models.BooleanField(
        verbose_name=_('Вид деятельности соответсвует шариату'),
        default=True
    )
    is_positive = models.BooleanField(
        verbose_name=_('Социальный анализ положителен'),
        default=False
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
        return str(self.client)
    
    def save(self, *args, **kwargs):
        # self.is_positive = check_client(instance=self)
        return super().save(*args, **kwargs)
