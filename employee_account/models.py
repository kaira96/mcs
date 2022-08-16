import email
from random import randint

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from company_structure.models import OfficeBranch, Position
from client.models import BOOL_CHOICES, GenderChoices, EducationChoices

from dateutil.relativedelta import relativedelta
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, login=None, password=None):
        """
        Creates and saves a Profile with the given login
        name and password.
        """

        if not login:
            raise ValueError('Users must have a login')
        user = self.model(
            login=login,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None):
        """
        Creates and saves a superuser with the given email,
        login and password.
        """
        user = self.create_user(
            login=login,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Employee(AbstractBaseUser):
    """
    the model describing the Employee
    """

    class Status(models.TextChoices):
        WORKS = 'WK', _('Работает')
        NOT_WORKS = 'NWK', _('Не работает')
        VACATION = 'VC', _('Отпуск')
        DECREE = 'DC', _('Декрет')
        MISSION = 'MS', _('Командировка')
        DISMISSED = 'DS', _('Уволен')
        SICK_LEAVE = 'SK', _('Больничный')

    login = models.CharField(
        max_length=125,
        unique=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name=_('Имя работника')
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_('Фамилия работника')
    )
    middle_name = models.CharField(
        max_length=255,
        verbose_name=_('Отчество работника'),
        default='',
        blank=True,
    )
    img = ResizedImageField(
        verbose_name=_('Фото сотрудника'),
        upload_to='avatar/%Y/%m/%d',
        default='avatar7.png',
        size=[400, 350],
        crop=['middle', 'center']
    )
    date_of_birth = models.DateField(
        verbose_name=_('Дата рождения'),
        null=True
        )
    passport = models.ForeignKey(
        'client.Passport',
        on_delete=models.PROTECT,
        related_name='employer',
        blank=True,
        null=True
    )
    phone_number = PhoneNumberField(
        verbose_name=_('Телефон номер клиента'),
        blank=True
    )
    email = models.EmailField(
        verbose_name=_('Адрес электронной почты')
    )
    address = models.CharField(
        verbose_name=_('Адрес проживания'),
        max_length=255,
    )
    registration_address = models.CharField(
        max_length=255,
        verbose_name=_('Адрес прописки'),
    )
    gender = models.CharField(
        max_length=2,
        verbose_name=_('Пол'),
        choices=GenderChoices.choices,
        blank=True
    )
    is_married = models.BooleanField(
        verbose_name=_('Семейное положение (Женат/Замужем)'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[0][0]
    )
    is_criminal_record = models.BooleanField(
        verbose_name=_('Есть ли судимость'),
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    education_status = models.CharField(
        max_length=3,
        verbose_name=_('Образование'),
        choices=EducationChoices.choices,
        blank=True
    )
    is_beneficiary = models.BooleanField(
        verbose_name='Являетесь ли вы бенефициарным собственником?',
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    is_political_man = models.BooleanField(
        verbose_name="Являетесь ли вы политически значимым человеком?",
        choices=BOOL_CHOICES,
        default=BOOL_CHOICES[1][0]
    )
    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status.WORKS,
        verbose_name=_('Статус')
    )
    is_active = models.BooleanField(
        default=True
    )
    is_admin = models.BooleanField(
        default=False
    )
    office_branch = models.OneToOneField(
        OfficeBranch,
        on_delete=models.PROTECT,
        verbose_name=_('Филиал/Офис'),
        blank=True,
        null=True
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания записи')
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи')
    )

    objects = UserManager()

    USERNAME_FIELD = 'login'
    
    def salary_calculation(self):   
        pass

    def bonus_calculation(self):
        pass
        
    def __str__(self):
        return str(self.full_name)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"

    @property
    def position(self):
        position = self.positions.filter(is_current=True).first()
        if position is None:
            return _('Нету позизции')
        return position

    def save(self, *args, **kwargs):

        # If the login field was not filled, then generate it
        if self.login == '':
            self.login = f'{self.first_name}.{self.last_name}.{randint(1, 9)}'

        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')

    # Setting verbose name for @property attributes
    full_name.fget.short_description = _('Полное имя ФИО')
    position.fget.short_description = _('Позиция')


class Salary(models.Model):
    salary = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Зарплата сотрудника в сомах')
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='salaries'
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_salary = self.salary

    def __str__(self):
        return str(self.salary)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Implementation of payroll update
        if self.previous_salary != self.salary:
            # If he did not have a record in the bonus amount model before,
            # the variable salary_obj will be None
            salary_obj = SalaryHistory.objects.filter(
                is_current=True, 
                employee=self.employee).first()

            # If there was an entry, update the data in the old entry.
            if salary_obj:
                salary_obj.end_date = timezone.now()
                salary_obj.is_current = False
                salary_obj.save()

            SalaryHistory(
                employee=self.employee,
                start_date=timezone.now(),
                salary=self.salary,                
                ).save()

    class Meta:
        verbose_name = _('Зарплата')
        verbose_name_plural = _('Зарплаты')
        
        
class SalaryHistory(models.Model):
    salary = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Зарплата сотрудника в сомах')
    )
    is_current = models.BooleanField(
        default=True,
        verbose_name=_('Актуальная зарплата?'),
        help_text=_('format: required, max_length=255')
    )
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата начала выдачи этой зарплаты'),
        help_text=_('format: required')
    )
    end_date = models.DateTimeField(
        default=timezone.datetime(
            year=2999,
            month=12,
            day=31,
            hour=12,
        ),
        verbose_name=_('Дата окончания выдачи этой зарплаты'),
        help_text=_('format: required')
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='salary_histories'
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
        return str(self.salary)

    class Meta:
        verbose_name = _('История зарплаты')
        verbose_name_plural = _('История зарплат')
        

class PositionHistory(models.Model):
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата начала работы на этой позиции'),
        help_text=_('format: required')
    )
    end_date = models.DateTimeField(
        default=timezone.datetime(
            year=2999,
            month=12,
            day=31,
            hour=12,
        ),
        verbose_name=_('Дата окончания работы на этой позиции'),
        help_text=_('format: required')
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        verbose_name=_('Позиция')
    )
    employee = models.ForeignKey(
        Employee,
        verbose_name=_('Сотрудник'),
        on_delete=models.PROTECT,
        related_name='positions'
    )
    is_current = models.BooleanField(
        default=True,
        verbose_name=_('Это актуальные данные'),
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
        return f"{self.employee}|{self.position}"

    class Meta:
        verbose_name = _('Хронология должности сотрудника')
        verbose_name_plural = _('Хронология должностей сотрудников')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.employee.positions.filter(is_current=True).update(is_current=False, end_date=timezone.now())
        self.pk = None
        super(PositionHistory, self).save(force_insert, force_update, using, update_fields)


class Bonus(models.Model):
    bonus_amount = models.PositiveIntegerField(
        verbose_name=_('Размер бонуса за одно финансирования'),
    )
    min_credit_quantity = models.PositiveSmallIntegerField(
        verbose_name=_('Минимальное кол-ва финансирования'),
    )
    position = models.OneToOneField(
        Position,
        on_delete=models.PROTECT,
        verbose_name=_('Позиция'),
        related_name='bonus'
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_bonus_amount = self.bonus_amount
        self.previous_min_credit_quantity = self.min_credit_quantity
            
    def __str__(self):
        return str(self.position) + ' | ' + str(self.bonus_amount)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Implementation of payroll update
        if self.previous_bonus_amount != self.bonus_amount or \
            self.previous_min_credit_quantity != self.min_credit_quantity:
            # If he did not have a record in the bonus amount model before,
            # the variable bonus_obj will be None
            bonus_obj = BonusHistory.objects.filter(
                is_active=True, 
                position=self.position).first()

            # If there was an entry, update the data in the old entry.
            if bonus_obj:
                bonus_obj.end_date = timezone.now()
                bonus_obj.is_active = False
                bonus_obj.save()

            BonusHistory(
                position=self.position,
                start_date=timezone.now(),
                bonus_amount=self.bonus_amount,
                min_credit_quantity=self.min_credit_quantity
                ).save()
    
    class Meta:
        verbose_name = _('Бонус')
        verbose_name_plural = _('Бонусы')
        

class BonusHistory(models.Model):
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        verbose_name=_('Позиция'),
        related_name='bonus_histories'
    )
    bonus_amount = models.PositiveIntegerField(
        verbose_name=_('Размер бонуса за одно финансирования'),
    )
    min_credit_quantity = models.PositiveSmallIntegerField(
        verbose_name=_('Минимальное кол-ва финансирования'),
    )
    is_active = models.BooleanField(
        verbose_name=_('Активный'),
        default=True,
    )
    start_date = models.DateTimeField(
        verbose_name=_('Дата началы действия размера бонуса')
    )
    end_date = models.DateTimeField(
        verbose_name=_('Дата конца действия размера бонуса'),
        default=timezone.datetime(
            year=2999,
            month=12,
            day=31,
            hour=12,
        ),  
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
        return str(self.position_id)
    
    class Meta:
        verbose_name = _('История бонуса')
        verbose_name_plural = _('История бонусов')
        

class DisciplinaryAction(models.Model):
    disciplinary_action_amount = models.DecimalField(
        verbose_name=_('Дисциплинарное взыскание в %'),
        validators=[MinValueValidator(0),
                    MaxValueValidator(1)],
        max_digits=3,
        decimal_places=2,
        default=0
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name=_('Сотрудник'),
        related_name='disciplinary_action'
     )
    disciplinary_action_period = models.PositiveSmallIntegerField(
        verbose_name=_('Срок дисциплинарного взыскания'),
        help_text=_('В месяцах')
    )
    is_active = models.BooleanField(
        verbose_name='Дисциплинарное взыскание есть',
        default=False
    )
    end_date = models.DateField(
        blank=True,
        verbose_name=_('Дата окончания взыскания'),
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
        return f'{self.disciplinary_action_amount} | {self.employee_id}'
    
    def save(self, *args, **kwargs):
        if self.disciplinary_action_period == 0:
            self.is_active = False
        self.end_date = timezone.now().today() + relativedelta(months=self.disciplinary_action_period)
        super().save(*args, **kwargs)
        DisciplinaryActionHistory.objects.create(
            disciplinary_action_amount=self.disciplinary_action_amount,
            employee=self.employee,
            disciplinary_action_period=self.disciplinary_action_period,
            is_active=self.is_active,
            end_date=self.end_date,
            created_date=self.created_date,
            updated_date=self.updated_date,
        )
    
    class Meta:
        verbose_name = _('Дисциплинарное взыскание')
        verbose_name_plural = _('Дисциплинарные взыскания')
        unique_together = ('employee_id', 'is_active')
      

class DisciplinaryActionHistory(models.Model):
    disciplinary_action_amount = models.DecimalField(
        verbose_name=_('Дисциплинарное взыскание в %'),
        validators=[MinValueValidator(0),
                    MaxValueValidator(1)],
        max_digits=3,
        decimal_places=2,
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name=_('Сотрудник'),
        related_name='disciplinary_action_histories'
     )
    disciplinary_action_period = models.PositiveSmallIntegerField(
        verbose_name=_('Срок дисциплинарного взыскания'),
        help_text=_('В месяцах')
    )
    is_active = models.BooleanField(
        verbose_name='Дисциплинарное взыскание есть',
    )
    end_date = models.DateField(
        verbose_name=_('Дата окончания взыскания'),
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
        return f'{self.disciplinary_action_amount} | {self.employee_id}'
    
    class Meta:
        verbose_name = _('История дисциплинарного взыскания')
        verbose_name_plural = _('История дисциплинарных взысканий')
