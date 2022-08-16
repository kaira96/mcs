from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
BOOL_CHOICES = ((True, _('Да')), (False, _('Нет')))


class GenderChoices(models.TextChoices):
    MAN = 'M', _('Мужчина')
    WOMAN = 'W', _('Женщина')
    
    
class EducationChoices(models.TextChoices):
    HIGHER = 'H', _('Высшее')
    MIDDLE = 'M', _('Среднее')
    NOT_COMPLETED_HIGHER = 'NCH', _('Не оконченное высшее')
    NOT_COMPLETED_MIDDLE = 'NCM', _('Не оконченное cреднее')
    
    
class Client(models.Model):
    first_name = models.CharField(
        max_length=255,
        verbose_name=_('имя клиента')
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_('Фамилия клиента')
    )
    middle_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Отчество клиента')
    )
    residence_address = models.CharField(
        max_length=255,
        verbose_name=_('Адрес проживания')
    )
    registration_address = models.CharField(
        max_length=255,
        verbose_name=_('Адрес прописки')
    )
    gender = models.CharField(
        max_length=2,
        verbose_name=_('Пол'),
        choices=GenderChoices.choices
    )
    is_married = models.BooleanField(
        verbose_name=_('Семейное положение (Холост / Не замужем)'),
        choices=BOOL_CHOICES
    )
    is_criminal_record = models.BooleanField(
        verbose_name=_('Есть ли судимость'),
        choices=BOOL_CHOICES
    )
    education_status = models.CharField(
        max_length=3,
        verbose_name=_('Образование'),
        choices=EducationChoices.choices
    )
    phone_number = PhoneNumberField(
        verbose_name=_('Телефон номер клиента')
    )
    contact_person_phone_numbers = models.CharField(
        max_length=255,
        verbose_name=_('Телефонные номера контактных лиц'),
        help_text=_('format: бабушка: 0500123456; дочь: 0500123456')
    )
    date_of_birth = models.DateField(
        verbose_name=_('Дата рождения')
    )
    passport = models.ForeignKey(
        'Passport',
        on_delete=models.PROTECT,
        related_name='client'
    )
    is_beneficiary = models.BooleanField(
        verbose_name='Являетесь ли вы бенефициарным собственником?',
        choices=BOOL_CHOICES,
    )
    is_political_man = models.BooleanField(
        verbose_name="Являетесь ли вы политически значимым человеком?",
        choices=BOOL_CHOICES
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"
    
    @property
    def get_age(self):
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    def __str__(self):
        return str(self.full_name)
    
    class Meta:
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')
        ordering = ('-created_date',)
        

class Passport(models.Model):
    series = models.CharField(
        max_length=7,
        verbose_name=_('Серия пасспорта'),
        blank=True
    )
    date_of_issue = models.DateField(
        verbose_name=_('Дата выдачи паспорта'),
        blank=True
    )
    pin = models.CharField(
        max_length=14,
        verbose_name=_('ПИН'),
        blank=True
    )
    issued_it = models.CharField(
        max_length=6,
        verbose_name=_('Номер'),
        blank=True,
    )
    series_type = models.CharField(
        max_length=2,
        verbose_name="Тип серии",
        choices=(("ID", 'ID'), ('AN', 'AN')),
        default='ID'
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
        return f"{self.series}|{self.pin}"

    class Meta:
        verbose_name = _('Паспорт')
        verbose_name_plural = _('Паспорта')
        ordering = ('-created_date',)
        

class Job(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='job',
        verbose_name=_('Клиент')
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Наименование организации')
    )
    address = models.CharField(
        max_length=255,
        verbose_name=_('Адрес организации')
    )
    position = models.CharField(
        max_length=255,
        verbose_name=_('Должность')
    )
    company_definition = models.CharField(
        max_length=255,
        verbose_name=_('Деятельность компании')
    )
    date_of_employment = models.DateField(
        verbose_name=_('Дата принятия на работу')
    )
    previous_job = models.CharField(
        max_length=255,
        verbose_name=_('Место предыдущей работы(1)'),
        default=_('Нету')
    )
    penultimate_job = models.CharField(
        max_length=255,
        verbose_name=_('Место предпоследний работы(2)'),
        default=_('Нету')
    )
    working_period_previous_job = models.PositiveIntegerField(
        verbose_name=_('Срок работы в месяцах(1)'),
        blank=True,
        default=0
    )
    working_period_penultimate_job = models.PositiveIntegerField(
        verbose_name=_('Срок работы в месяцах(2)'),
        blank=True,
        default=0
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
        return f"{self.client}|{self.name}"

    class Meta:
        verbose_name = _('Работу клиента')
        verbose_name_plural = _('Работы клиентов')
        ordering = ('-created_date',)


class ClientSalary(models.Model):
    salary = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Доход за вычетом налогов'),
        help_text=_('Сом в мес.'),
        validators=[MinValueValidator(0)]
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
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='client_salary'
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
        return f"{self.client}|{self.salary}"

    class Meta:
        verbose_name = _('Доход клиента')
        verbose_name_plural = _('Доходы клиентов')
        ordering = ('-created_date',)


class Dependent(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='dependet',
        verbose_name=_('Клиент')
    )
    children_under_18 = models.PositiveIntegerField(
        verbose_name=_('Количество детей младше 18 лет'),
        default=0
    )
    children_over_18 = models.PositiveIntegerField(
        verbose_name=_('Количество детей старше 18 лет'),
        default=0
    )
    ages = models.CharField(
        verbose_name='Возраста',
        max_length=255,
        blank=True
    )
    another_dependents = models.PositiveSmallIntegerField(
        verbose_name=_('Количество других иждивенцев'),
        default=0
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )

    def clean(self):

        errors = []

        for elem in self.ages:
            if not elem.isdigit() and elem != ',':
                errors.append(ValidationError({'ages': "Не правильный формат. Должно быть (14,6,22)"}))
                break

        total_children = self.children_under_18 + self.children_over_18

        children_ages_count = len([i for i in self.ages.split(',') if i.isdigit()])

        if children_ages_count < total_children:
            errors.append(ValidationError({'ages': "Не все возраста заполнены"}))

        if children_ages_count > total_children:
            errors.append(ValidationError({'ages': "Cлишком много возрастов"}))

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return str(self.client)

    class Meta:
        verbose_name = _('Иждевенец')
        verbose_name_plural = _('Иждевенцы')
        ordering = ('-created_date',)


class Spouse(models.Model):
    first_name = models.CharField(
        max_length=255,
        verbose_name=_('Имя супруги/а'),
        blank=True
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_('Фамилия супруги/а'),
        blank=True
    )
    middle_name = models.CharField(
        max_length=255,
        verbose_name=_('Отчество супруги/а'),
        blank=True
    )
    passport = models.ForeignKey(
        Passport,
        on_delete=models.PROTECT,
        related_name='spouse',
        blank=True,
        verbose_name=_('Пасспорт')
    )
    residence_address = models.CharField(
        max_length=255,
        verbose_name=_('Адрес проживания'),
        blank=True
    )
    gender = models.CharField(
        max_length=2,
        verbose_name=_('Пол'),
        choices=GenderChoices.choices,
        blank=True
    )
    phone_number = PhoneNumberField(
        verbose_name=_('Телефон номер супруги/а'),
        blank=True
    )
    job_name = models.CharField(
        max_length=255,
        verbose_name=_('Место работы'),
        blank=True
    )
    job_position = models.CharField(
        max_length=255,
        verbose_name=_('Должность'),
        blank=True
    )
    education_status = models.CharField(
        max_length=3,
        verbose_name=_('Образование'),
        choices=EducationChoices.choices,
        blank=True
    )
    is_guarantor = models.BooleanField(
        verbose_name=_('Супруг/а будет поручителем?'),
        choices=BOOL_CHOICES,
        blank=True
    )
    salary = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Доход за вычетом налогов'),
        help_text=_('Сом в мес.'),
        blank=True,
        validators=[MinValueValidator(0)],
    )
    client = models.OneToOneField(
        Client,
        on_delete=models.PROTECT,
        blank=True,
        related_name='spouse',
        verbose_name=_('Клиент')
    )
    date_of_birth = models.DateField(
        verbose_name=_('Дата рождения'),
        blank=True,
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )
    

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"

    def __str__(self):
        return f"{self.client}|{self.full_name}"

    class Meta:
        verbose_name = _('Супруг/а')
        verbose_name_plural = _('Супруги')
        ordering = ('-created_date',)


class Guarantor(models.Model):
    first_name = models.CharField(
        max_length=255,
        verbose_name=_('Имя поручителя'),
        blank=True
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_('Фамилия поручителя'),
        blank=True
    )
    middle_name = models.CharField(
        max_length=255,
        verbose_name=_('Отчество поручителя'),
        blank=True
    )
    passport = models.ForeignKey(
        Passport,
        on_delete=models.PROTECT,
        related_name='guarantor',
        blank=True,
        verbose_name=_('Пасспорт')
    )
    residence_address = models.CharField(
        max_length=255,
        verbose_name=_('Адрес проживания'),
        blank=True
    )
    gender = models.CharField(
        max_length=2,
        verbose_name=_('Пол'),
        choices=GenderChoices.choices,
        blank=True
    )
    phone_number = PhoneNumberField(
        verbose_name=_('Телефон номер поручителя'),
        blank=True
    )
    job_name = models.CharField(
        max_length=255,
        verbose_name=_('Место работы'),
        blank=True
    )
    education_status = models.CharField(
        max_length=3,
        verbose_name=_('Оброзование'),
        choices=EducationChoices.choices,
        blank=True
    )
    job_position = models.CharField(
        max_length=255,
        verbose_name=_('Должность'),
        blank=True
    )
    salary = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Доход за вычетом налогов'),
        help_text=_('сом мес.'),
        blank=True,
        validators=[MinValueValidator(0)],
    )
    client = models.OneToOneField(
        Client,
        on_delete=models.PROTECT,
        blank=True,
        verbose_name=_('Клиент'),
        related_name='guarantor'
    )
    date_of_birth = models.DateField(
        verbose_name=_('Дата рождения'),
        blank=True
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата обновления записи'),
        auto_now=True
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"

    def __str__(self):
        return f"{self.client}|{self.full_name}"

    class Meta:
        verbose_name = _('Поручитель')
        verbose_name_plural = _('Поручители')
        ordering = ('-created_date',)


class ClientSpend(models.Model):
    title = models.CharField(
        verbose_name=_("Название расхода"),
        max_length=50,
        unique=True
    )
    per_month_amount = models.DecimalField(
        verbose_name=_("Сумма расхода за мес."),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    description = models.CharField(
        verbose_name=_("Краткое описание расхода"),
        max_length=500,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Активный"),
        default=True
    )
    created_date = models.DateTimeField(
        verbose_name=_('дата создания записи'),
        auto_now_add=True,
    )
    updated_date = models.DateTimeField(
        verbose_name=_('дата обновления записи'),
        auto_now=True
    )
    
    def __str__(self) -> str:
        return str(self.title)
    
    class Meta:
        verbose_name = _('Расход клиента')
        verbose_name_plural = _('Расходы клиентов')
        ordering = ('-created_date',)


class ClientCommercial(models.Model):
    salary = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Доходы(чистая прибыль)'),
        help_text=_('сом/мес')
    )
    company_name = models.CharField(
        max_length=255,
        verbose_name=_('Наименование орг.'),
    )
    organization_information = models.CharField(
        max_length=255,
        verbose_name=_('Деятельность организации')
    )
    address = models.CharField(
        max_length=255,
        verbose_name=_('Адрес организации')
    )
    license_number = models.CharField(
        max_length=255,
        verbose_name=_('№ИНН/патента/свидетельство')
    )
    position = models.CharField(
        max_length=255,
        verbose_name=_('Должность')
    )
    start_date = models.DateField(
        verbose_name=_('Дата начала деятельности')
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='client_commercial',
        verbose_name=_('Клиент')
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
        return f"{self.client}|{self.full_name}"

    class Meta:
        verbose_name = _('Комерческий клиент')
        verbose_name_plural = _('Комерческие клиенты')
        ordering = ('-created_date',)
