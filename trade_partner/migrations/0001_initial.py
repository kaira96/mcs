# Generated by Django 4.0.6 on 2022-08-04 09:41

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import trade_partner.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('loan_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Название категории')),
                ('is_active', models.BooleanField(default=True, verbose_name='Данная категория активна?')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='trade_partner.category', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товаров',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='TradePartner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название торговой организации')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен ли данный партнер')),
                ('bank_id_code', models.CharField(max_length=8, validators=[trade_partner.validators.only_int], verbose_name='БИК банка')),
                ('merchant_account_number', models.CharField(max_length=25, validators=[trade_partner.validators.only_int], verbose_name='Номер счета торговой организации')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
            ],
            options={
                'verbose_name': 'Торговая организация',
                'verbose_name_plural': 'Торговые организации',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость товара')),
                ('seller_full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='ФИО продавца')),
                ('seller_phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон продавца')),
                ('first_installment_is_paid_to_TO', models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], verbose_name='Первоначальный платеж оплачивается в кассе ТО')),
                ('filial_point', models.CharField(max_length=255, verbose_name='Точка филлиала')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trade_partner.category', verbose_name='Категория товара')),
                ('loan_application', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_buy', to='loan_system.loanapplication')),
                ('trade_partner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trade_partner.tradepartner', verbose_name='Торговая организация')),
            ],
            options={
                'verbose_name': 'Информация о приобритаемом товаре',
                'verbose_name_plural': 'Информации о приобритаемых товарах',
                'ordering': ('-created_date',),
            },
        ),
    ]
