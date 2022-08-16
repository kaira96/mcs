from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

# Create your models here.
class Account(models.Model):
    number = models.CharField(
        max_length=20,
        verbose_name=_('Номер счёта')
    )
    name = models.CharField(
        max_length=500,
        verbose_name=_('Название счёта')
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
        return str(self.number)
    
    class Meta:
        verbose_name = _('Счёт')
        verbose_name_plural = _('Счета')
        ordering = ['number']
        

class Transaction(models.Model):
    unique_code = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        verbose_name=_('Уникальный код транзакции')
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP-address от кого прошла данная транзакция')
    )
    debit = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        verbose_name=_('От счёта'),
        related_name='debit_transaction'
    )
    credit = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        verbose_name=_('На счёт'),
        related_name='credit_transaction'
    )
    amount = models.DecimalField(
        max_digits=50,
        decimal_places=2,
        verbose_name=_('Сумма'),
        validators=[MinValueValidator(0)],
    )
    description = models.CharField(
        max_length=2000,
        verbose_name=_('Описание транзакции')
    )
    branch = models.ForeignKey(
        'company_structure.OfficeBranch',
        on_delete=models.PROTECT,
        verbose_name=_('Филиал')
    )
    employee = models.ForeignKey(
        'employee_account.Employee',
        on_delete=models.PROTECT
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
        return f'{self.debit} -> {self.credit}'
    
    class Meta:
        verbose_name = _('Транзакция')
        verbose_name_plural = _('Транзакции')
        ordering = ['-created_date']
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        debit = Balance(
            account=self.debit,
            debit_amount=self.amount,
            branch=self.branch,
            employee=self.employee
        )
        credit = Balance(
            account=self.credit,
            credit_amount=self.amount,
            branch=self.branch,
            employee=self.employee
        )
        return Balance.objects.bulk_create(
            (debit, credit)
        )
        

class Balance(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        verbose_name=_('Номер счёта')
    )
    debit_amount = models.DecimalField(
        max_digits=50,
        decimal_places=2,
        verbose_name=_('Дебит'),
        validators=[MinValueValidator(0)],
        default=0
    )
    credit_amount = models.DecimalField(
        max_digits=50,
        decimal_places=2,
        verbose_name=_('Кредит'),
        validators=[MinValueValidator(0)],
        default=0
    )
    branch = models.ForeignKey(
        'company_structure.OfficeBranch',
        on_delete=models.PROTECT,
        verbose_name=_('Филиал')
    )
    employee = models.ForeignKey(
        'employee_account.Employee',
        on_delete=models.PROTECT
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
        return str(self.account)
    
    class Meta:
        verbose_name = _('Баланс')
        verbose_name_plural = _('Баланс')
        ordering = ['-created_date']