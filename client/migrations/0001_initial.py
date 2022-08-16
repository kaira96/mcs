# Generated by Django 4.0.6 on 2022-08-04 09:41

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='имя клиента')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия клиента')),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество клиента')),
                ('residence_address', models.CharField(max_length=255, verbose_name='Адрес проживания')),
                ('registration_address', models.CharField(max_length=255, verbose_name='Адрес прописки')),
                ('gender', models.CharField(choices=[('M', 'Мужчина'), ('W', 'Женщина')], max_length=2, verbose_name='Пол')),
                ('is_married', models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], verbose_name='Семейное положение (Холост / Не замужем)')),
                ('is_criminal_record', models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], verbose_name='Есть ли судимость')),
                ('education_status', models.CharField(choices=[('H', 'Высшее'), ('M', 'Среднее'), ('NCH', 'Не оконченное высшее'), ('NCM', 'Не оконченное cреднее')], max_length=3, verbose_name='Образование')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон номер клиента')),
                ('contact_person_phone_numbers', models.CharField(help_text='format: бабушка: 0500123456; дочь: 0500123456', max_length=255, verbose_name='Телефонные номера контактных лиц')),
                ('date_of_birth', models.DateField(verbose_name='Дата рождения')),
                ('is_beneficiary', models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], verbose_name='Являетесь ли вы бенефициарным собственником?')),
                ('is_political_man', models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], verbose_name='Являетесь ли вы политически значимым человеком?')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='ClientSpend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название расхода')),
                ('per_month_amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма расхода за мес.')),
                ('description', models.CharField(blank=True, max_length=500, verbose_name='Краткое описание расхода')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='дата обновления записи')),
            ],
            options={
                'verbose_name': 'Расход клиента',
                'verbose_name_plural': 'Расходы клиентов',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(blank=True, max_length=7, verbose_name='Серия пасспорта')),
                ('date_of_issue', models.DateField(blank=True, verbose_name='Дата выдачи паспорта')),
                ('pin', models.CharField(blank=True, max_length=14, verbose_name='ПИН')),
                ('issued_it', models.CharField(blank=True, max_length=6, verbose_name='Номер')),
                ('series_type', models.CharField(choices=[('ID', 'ID'), ('AN', 'AN')], default='ID', max_length=2, verbose_name='Тип серии')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
            ],
            options={
                'verbose_name': 'Паспорт',
                'verbose_name_plural': 'Паспорта',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='Spouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name='Имя супруги/а')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='Фамилия супруги/а')),
                ('middle_name', models.CharField(blank=True, max_length=255, verbose_name='Отчество супруги/а')),
                ('residence_address', models.CharField(blank=True, max_length=255, verbose_name='Адрес проживания')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Мужчина'), ('W', 'Женщина')], max_length=2, verbose_name='Пол')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Телефон номер супруги/а')),
                ('job_name', models.CharField(blank=True, max_length=255, verbose_name='Место работы')),
                ('job_position', models.CharField(blank=True, max_length=255, verbose_name='Должность')),
                ('education_status', models.CharField(blank=True, choices=[('H', 'Высшее'), ('M', 'Среднее'), ('NCH', 'Не оконченное высшее'), ('NCM', 'Не оконченное cреднее')], max_length=3, verbose_name='Образование')),
                ('is_guarantor', models.BooleanField(blank=True, choices=[(True, 'Да'), (False, 'Нет')], verbose_name='Супруг/а будет поручителем?')),
                ('salary', models.DecimalField(blank=True, decimal_places=2, help_text='Сом в мес.', max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Доход за вычетом налогов')),
                ('date_of_birth', models.DateField(blank=True, verbose_name='Дата рождения')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('client', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='spouse', to='client.client', verbose_name='Клиент')),
                ('passport', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='spouse', to='client.passport', verbose_name='Пасспорт')),
            ],
            options={
                'verbose_name': 'Супруг/а',
                'verbose_name_plural': 'Супруги',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование организации')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес организации')),
                ('position', models.CharField(max_length=255, verbose_name='Должность')),
                ('company_definition', models.CharField(max_length=255, verbose_name='Деятельность компании')),
                ('date_of_employment', models.DateField(verbose_name='Дата принятия на работу')),
                ('previous_job', models.CharField(default='Нету', max_length=255, verbose_name='Место предыдущей работы(1)')),
                ('penultimate_job', models.CharField(default='Нету', max_length=255, verbose_name='Место предпоследний работы(2)')),
                ('working_period_previous_job', models.PositiveIntegerField(blank=True, default=0, verbose_name='Срок работы в месяцах(1)')),
                ('working_period_penultimate_job', models.PositiveIntegerField(blank=True, default=0, verbose_name='Срок работы в месяцах(2)')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='job', to='client.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Работу клиента',
                'verbose_name_plural': 'Работы клиентов',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='Guarantor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name='Имя поручителя')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='Фамилия поручителя')),
                ('middle_name', models.CharField(blank=True, max_length=255, verbose_name='Отчество поручителя')),
                ('residence_address', models.CharField(blank=True, max_length=255, verbose_name='Адрес проживания')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Мужчина'), ('W', 'Женщина')], max_length=2, verbose_name='Пол')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Телефон номер поручителя')),
                ('job_name', models.CharField(blank=True, max_length=255, verbose_name='Место работы')),
                ('education_status', models.CharField(blank=True, choices=[('H', 'Высшее'), ('M', 'Среднее'), ('NCH', 'Не оконченное высшее'), ('NCM', 'Не оконченное cреднее')], max_length=3, verbose_name='Оброзование')),
                ('job_position', models.CharField(blank=True, max_length=255, verbose_name='Должность')),
                ('salary', models.DecimalField(blank=True, decimal_places=2, help_text='сом мес.', max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Доход за вычетом налогов')),
                ('date_of_birth', models.DateField(blank=True, verbose_name='Дата рождения')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('client', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='guarantor', to='client.client', verbose_name='Клиент')),
                ('passport', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='guarantor', to='client.passport', verbose_name='Пасспорт')),
            ],
            options={
                'verbose_name': 'Поручитель',
                'verbose_name_plural': 'Поручители',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('children_under_18', models.PositiveIntegerField(default=0, verbose_name='Количество детей младше 18 лет')),
                ('children_over_18', models.PositiveIntegerField(default=0, verbose_name='Количество детей старше 18 лет')),
                ('ages', models.CharField(blank=True, max_length=255, verbose_name='Возраста')),
                ('another_dependents', models.PositiveSmallIntegerField(default=0, verbose_name='Количество других иждивенцев')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dependet', to='client.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Иждевенец',
                'verbose_name_plural': 'Иждевенцы',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='ClientSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.DecimalField(decimal_places=2, help_text='Сом в мес.', max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Доход за вычетом налогов')),
                ('is_current', models.BooleanField(default=True, help_text='format: required, max_length=255', verbose_name='Актуальная зарплата?')),
                ('start_date', models.DateTimeField(auto_now_add=True, help_text='format: required', verbose_name='Дата начала выдачи этой зарплаты')),
                ('end_date', models.DateTimeField(default=datetime.datetime(2999, 12, 31, 12, 0), help_text='format: required', verbose_name='Дата окончания выдачи этой зарплаты')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_salary', to='client.client')),
            ],
            options={
                'verbose_name': 'Доход клиента',
                'verbose_name_plural': 'Доходы клиентов',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='ClientCommercial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.DecimalField(decimal_places=2, help_text='сом/мес', max_digits=8, verbose_name='Доходы(чистая прибыль)')),
                ('company_name', models.CharField(max_length=255, verbose_name='Наименование орг.')),
                ('organization_information', models.CharField(max_length=255, verbose_name='Деятельность организации')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес организации')),
                ('license_number', models.CharField(max_length=255, verbose_name='№ИНН/патента/свидетельство')),
                ('position', models.CharField(max_length=255, verbose_name='Должность')),
                ('start_date', models.DateField(verbose_name='Дата начала деятельности')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_commercial', to='client.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Комерческий клиент',
                'verbose_name_plural': 'Комерческие клиенты',
                'ordering': ('-created_date',),
            },
        ),
        migrations.AddField(
            model_name='client',
            name='passport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client', to='client.passport'),
        ),
    ]