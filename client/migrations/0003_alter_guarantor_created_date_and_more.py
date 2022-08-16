# Generated by Django 4.0.6 on 2022-07-25 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_client_options_alter_clientsalary_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guarantor',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи'),
        ),
        migrations.AlterField(
            model_name='guarantor',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи'),
        ),
        migrations.AlterField(
            model_name='spouse',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи'),
        ),
        migrations.AlterField(
            model_name='spouse',
            name='date_of_birth',
            field=models.DateField(blank=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='spouse',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи'),
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
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_commercial', to='client.client')),
            ],
            options={
                'verbose_name': 'Комерческий клиент',
                'verbose_name_plural': 'Комерческие клиенты',
                'ordering': ('-created_date',),
            },
        ),
    ]