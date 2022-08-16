# Generated by Django 4.0.6 on 2022-08-04 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting_balance', '0001_initial'),
        ('company_structure', '0001_initial'),
        ('client', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('account_number', models.BigAutoField(db_index=True, editable=False, primary_key=True, serialize=False, unique=True)),
                ('current_balance', models.PositiveBigIntegerField(default=0, verbose_name='Текущий баланс депозитного счёта')),
                ('date_of_last_deposit', models.DateTimeField(blank=True, verbose_name='Дата последнего пополнения')),
                ('is_active', models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], default=True, verbose_name='Активный счёт')),
                ('is_blocked', models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], default=False, verbose_name='Заблакирован счёт')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('balance_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting_balance.account', verbose_name='Балансовый счёт')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company_structure.officebranch', verbose_name='Филиал')),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='my_deposit_account', to='client.client', verbose_name='Клиент')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Депозитный счёт',
                'verbose_name_plural': 'Депозитные счёта',
                'ordering': ('-created_date',),
            },
        ),
    ]
