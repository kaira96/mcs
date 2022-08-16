from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from client.models import BOOL_CHOICES
# from accounting_balance.models import AccountTransactionTemplates, Transaction, AccountTransactionTemplate


# Create your models here.
class MoneyTransfer(models.Model):
    trade_partner = models.ForeignKey(
        'trade_partner.TradePartner',
        verbose_name=_('Торговая организация'),
        on_delete=models.PROTECT,
        related_name='my_money_transfers'
    )
    loan = models.OneToOneField(
        'loan_system.Loan',
        verbose_name=_('Кредит'),
        on_delete=models.PROTECT,
        related_name='money_transfer'
    )
    employee = models.ForeignKey(
        'employee_account.Employee',
        on_delete=models.PROTECT,
        verbose_name=_('Сотрудник'),
        related_name='my_employee_transfers'
    )
    branch = models.ForeignKey(
        'company_structure.OfficeBranch',
        on_delete=models.PROTECT,
        verbose_name=_('Филиал'),
        related_name='my_branch_transfers'
    )
    transfer_amount = models.DecimalField(
        verbose_name=_('Сумма перевода'),
        validators=[MinValueValidator(0)],
        max_digits=12,
        decimal_places=2,
    )
    is_transfered = models.BooleanField(
        verbose_name=_('Средства переведены ТО'),
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
        self.real_not_transfered = True
    
    # def save(self, *args, **kwargs):
    #     # if self.real_not_transfered and self.is_transfered:
    #     #     transaction_template = AccountTransactionTemplate.objects.get(
    #     #         transaction_template=AccountTransactionTemplates.payment_for_trade_partner
    #     #     )
    #     #     description_template = ...
    #     #     transaction = Transaction(
    #     #         ip_address=...,
    #     #         debit=transaction_template.from_account,
    #     #         credit=transaction_template.to_account,
    #     #         amount=self.transfer_amount,
    #     #         description=description_template,
    #     #         branch=self.branch,
    #     #         employee=...
    #     #     )
    #     #     transaction.save()
    #     return super().save(*args, **kwargs)
    
    def __str__(self):
        return _('Перевод № ') + str(self.id)
    
    class Meta:
        verbose_name = _('Перевод')
        verbose_name_plural = _('Переводы')
        ordering = ('-created_date',)
