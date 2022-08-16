from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from client.models import BOOL_CHOICES
from accounting_balance.models import AccountTransactionTemplate, AccountTransactionTemplates, Transaction


# Create your models here.
class Deposit(models.Model):
    account_number = models.BigAutoField(
        editable=False,
        unique=True,
        primary_key=True,
        db_index=True,
    )
    balance_account = models.ForeignKey(
        'accounting_balance.Account',
        on_delete=models.PROTECT,
        verbose_name=_('Балансовый счёт'),
    )
    client = models.OneToOneField(
        'client.Client',
        on_delete=models.PROTECT,
        verbose_name=_('Клиент'),
        related_name='my_deposit_account'
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
    current_balance = models.PositiveBigIntegerField(
        verbose_name=_('Текущий баланс депозитного счёта'),
        default=0
    )
    date_of_last_deposit = models.DateTimeField(
        verbose_name=_('Дата последнего пополнения'),
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name=_('Активный счёт'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[0][0]
    )
    is_blocked = models.BooleanField(
        verbose_name=_('Заблакирован счёт'),
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev_balance_amount = self.current_balance
    
    def save(self, request=None, *args, **kwargs):
        if self.created_date is None:
            self.date_of_last_deposit = timezone.now()
            
        if self.prev_balance_amount != self.current_balance and request:
            if self.current_balance > self.prev_balance_amount:
                self.date_of_last_deposit = timezone.now()
                
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

                if x_forwarded_for:
                    ipaddress = x_forwarded_for.split(',')[-1].strip()
                else:
                    ipaddress = request.META.get('REMOTE_ADDR')
                
                
                transaction_template = get_object_or_404(
                            AccountTransactionTemplate, 
                            transaction_template=AccountTransactionTemplates.repayment_of_financing_by_the_borrower
                            )
                
                description_template = _('Пополнение ') + str(self) + _(' на сумму ') + str(balance := self.current_balance - self.prev_balance_amount)
                
                transaction = Transaction(
                            ip_address=ipaddress,
                            debit=transaction_template.from_account,
                            credit=transaction_template.to_account,
                            amount=balance,
                            description=f'{transaction_template.get_transaction_template_display()} ' + description_template,
                            branch=self.branch,
                            employee=self.employee
                        )
                transaction.save()
            
            elif self.prev_balance_amount > self.current_balance:
                self.current_balance = self.prev_balance_amount
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return _('Депозитный счёт № ') + str(self.account_number)
    
    class Meta:
        verbose_name = _('Депозитный счёт')
        verbose_name_plural = _('Депозитные счёта')
        ordering = ('-created_date',)
        