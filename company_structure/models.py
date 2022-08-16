from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.utils import OperationalError, ProgrammingError

from phonenumber_field.modelfields import PhoneNumberField


class City(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Название города'),
        help_text=_('format: required, max_length=255'),
        unique=True
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
        ordering = ('-created_date',)


class Region(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Название региона/района'),
        help_text=_('format: required, max_length=255'),
        unique=True 
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Регион/Район')
        verbose_name_plural = _('Регионы/Районы')
        ordering = ('-created_date',)


class Address(models.Model):
    city = models.ForeignKey(
        City, 
        on_delete=models.PROTECT
        )
    region = models.ForeignKey(
        Region, 
        on_delete=models.PROTECT
        )
    street = models.CharField(
        max_length=255,
        verbose_name=_('Улица'),
        help_text=_('format: required, max_length=255')
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )

    def __str__(self):
        return f'{self.region} {self.city} {self.street}'

    class Meta:
        verbose_name = _('Адрес')
        verbose_name_plural = _('Адресы')
        unique_together = ('city', 'region', 'street')
        ordering = ('-created_date',)


class OfficeBranch(models.Model):
    is_working = models.BooleanField(
        verbose_name=_('Работает ли офис'),
        help_text=_('format: required, True=works'),
        default=True
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='offices',
        verbose_name=_('Адрес офиса')
    )
    phone_number = PhoneNumberField(
        verbose_name=_('Телефонный номер офиса')
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Название офиса')
    )
    departments = models.ManyToManyField(
        'Department',
        verbose_name=_('Департаменты/Отделы'),
        related_name='office'
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        unique_together = ('name', 'address',)
        verbose_name = _('Филиал')
        verbose_name_plural = _('Филиалы')
        ordering = ('-created_date',)


class Department(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Название департамента'),
        unique=True
    )
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания департамента'),
        help_text=_('format: required')
    )
    end_date = models.DateTimeField(
        default=timezone.datetime(
            year=2999,
            month=12,
            day=31,
            hour=12,
        ),
        verbose_name=_('Дата закрытия департамента'),
        help_text=_('format: required')
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи')
    )
    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Департамент/Отдел')
        verbose_name_plural = _('Департаменты/Отделы')
        ordering = ('-created_date',)


class Position(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Название должности'),
        help_text=_('format: required, max_length=255')
    )
    department = models.ForeignKey(
        Department,
        verbose_name=_('Департамент/Отдел где работает'),
        on_delete=models.PROTECT,
        related_name='department'
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )

    def __str__(self):
        return f'{self.name}|{self.department.name}'

    class Meta:
        unique_together = ('name', 'department')
        verbose_name = _('Должность')
        verbose_name_plural = _('Должности')


class Holiday(models.Model):
    name = models.CharField(
        verbose_name=_("Название праздника"),
        max_length=100
    )
    date = models.DateField(
        verbose_name=_("Дата праздника"),
        unique=True
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
        
    def reset_holidays(self):
        HOLIDAYS = {}
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.date.year == timezone.now().year:
            HOLIDAYS[self.date] = self.name
        
    def __str__(self):
        return str(self.name) + ' | ' + str(self.date)
    
    class Meta:
        verbose_name = _('Праздник')
        verbose_name_plural = _('Праздники')
        ordering = ('-created_date',)


class WorkTime(models.Model):
    branch = models.OneToOneField(
        OfficeBranch,
        on_delete=models.PROTECT,
        verbose_name=_('Филиал')
    )
    start_time = models.TimeField(
        verbose_name=_('Время открытия филиала')
    )
    end_time = models.TimeField(
        verbose_name=_('Время закрытия филиала')
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __str__(self):
        return f'{self.branch} -> {self.start_time} :: {self.end_time}'
    
    class Meta:
        verbose_name = _('Время работы филиала')
        verbose_name_plural = _('Время работы филиалов')
        ordering = ('-created_date',)


try:
    holidays = Holiday.objects.filter(date__year=timezone.now().year).values('date', 'name')
    HOLIDAYS = {holiday['date']:holiday['name'] for holiday in holidays}
except OperationalError:
    HOLIDAYS = {}
except ProgrammingError:
    HOLIDAYS = {}
    