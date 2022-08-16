# Generated by Django 4.0.6 on 2022-08-04 17:45

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company_structure', '0001_initial'),
        ('loan_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanLimitAmountHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Лимит суммы финансирования на данную позицию')),
                ('is_current', models.BooleanField(default=True, help_text='format: required, max_length=255', verbose_name='Актуальный лимит?')),
                ('start_date', models.DateTimeField(auto_now_add=True, help_text='format: required', verbose_name='Дата начала лимита')),
                ('end_date', models.DateTimeField(default=datetime.datetime(2999, 12, 31, 12, 0), help_text='format: required', verbose_name='Дата окончания этого лимита')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company_structure.position', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'История лимита финансирования без акцепта кредитного коммитета',
                'verbose_name_plural': 'История лимитов финансирования без акцепта кредитного коммитета',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='LoanLimitAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Лимит суммы финансирования на данную позицию')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('position', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='company_structure.position', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Лимит финансирования без акцепта кредитного коммитета',
                'verbose_name_plural': 'Лимиты финансирования без акцепта кредитного коммитета',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='LoanInitialPaymentValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма приобретаемого товара (от этой суммы будет             считаться сумма первоначального взноса)')),
                ('initial_payment_percent', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='% Первоначального взноса от указанной суммы приобретаемого товара')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
            ],
            options={
                'verbose_name': 'Плановая сумма для первоначального взноса',
                'verbose_name_plural': 'Плановые суммы для первоначального взноса',
                'ordering': ('-created_date',),
                'unique_together': {('total_cost', 'initial_payment_percent')},
            },
        ),
    ]
