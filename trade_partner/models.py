from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from client.models import BOOL_CHOICES

from .validators import only_int


# Create your models here.
class TradePartner(models.Model):
    name = models.CharField(
        verbose_name=_('Название торговой организации'),
        max_length=255,
    )
    is_active = models.BooleanField(
        verbose_name=_('Активен ли данный партнер'),
        default=True
    )
    bank_id_code = models.CharField(
        verbose_name=_('БИК банка'),
        max_length=8,
        validators=[only_int]
    )
    merchant_account_number = models.CharField(
        verbose_name=_('Номер счета торговой организации'),
        max_length=25,
        validators=[only_int]
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
        return self.name

    class Meta:
        verbose_name = _('Торговая организация')
        verbose_name_plural = _('Торговые организации')
        ordering = ('-created_date',)


class Category(models.Model):
    name = models.CharField(
        verbose_name=_('Название категории'),
        max_length=255,
        db_index=True
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.PROTECT,
        verbose_name=_("Родительская категория")
    )
    is_active = models.BooleanField(
        verbose_name=_('Данная категория активна?'),
        default=True
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
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])
    
    class Meta:
        verbose_name = _("Категория товара")
        verbose_name_plural = _("Категории товаров")
        ordering = ('-created_date',)


class ProductDetail(models.Model):
    loan_application = models.ForeignKey(
        'loan_system.LoanApplication',
        on_delete=models.PROTECT,
        related_name='product_buy'
    )
    trade_partner = models.ForeignKey(
        TradePartner,
        verbose_name=_('Торговая организация'),
        on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('Категория товара'),
        on_delete=models.PROTECT
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_('Описание товара'),
    )
    price = models.DecimalField(
        verbose_name=_('Стоимость товара'),
        max_digits=10,
        decimal_places=2,
    )
    seller_full_name = models.CharField(
        verbose_name=_('ФИО продавца'),
        max_length=255,
        blank=True,
        null=True
    )
    seller_phone_number = PhoneNumberField(
        verbose_name=_('Телефон продавца'),
        blank=True,
        null=True
    )
    first_installment_is_paid_to_TO = models.BooleanField(
        verbose_name=_('Первоначальный платеж оплачивается в кассе ТО'),
        choices=BOOL_CHOICES,
    )
    filial_point = models.CharField(
        verbose_name=_('Точка филлиала'),
        max_length=255
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
        return str(self.loan_application)
    
    class Meta:
        verbose_name = _('Информация о приобритаемом товаре')
        verbose_name_plural = _('Информации о приобритаемых товарах')
        ordering = ('-created_date',)
