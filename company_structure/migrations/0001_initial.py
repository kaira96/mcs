# Generated by Django 4.0.6 on 2022-08-04 09:41

import datetime
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format: required, max_length=255', max_length=255, unique=True, verbose_name='Название города')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название департамента')),
                ('start_date', models.DateTimeField(auto_now_add=True, help_text='format: required', verbose_name='Дата создания департамента')),
                ('end_date', models.DateTimeField(default=datetime.datetime(2999, 12, 31, 12, 0), help_text='format: required', verbose_name='Дата закрытия департамента')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Департамент/Отдел',
                'verbose_name_plural': 'Департаменты/Отделы',
            },
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название праздника')),
                ('date', models.DateField(unique=True, verbose_name='Дата праздника')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
            ],
            options={
                'verbose_name': 'Праздник',
                'verbose_name_plural': 'Праздники',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format: required, max_length=255', max_length=255, unique=True, verbose_name='Название региона/района')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
            ],
            options={
                'verbose_name': 'Регион/Район',
                'verbose_name_plural': 'Регионы/Районы',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(help_text='format: required, max_length=255', max_length=255, verbose_name='Улица')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company_structure.city')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company_structure.region')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адресы',
                'unique_together': {('city', 'region', 'street')},
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format: required, max_length=255', max_length=255, verbose_name='Название должности')),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='department', to='company_structure.department', verbose_name='Департамент/Отдел где работает')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
                'unique_together': {('name', 'department')},
            },
        ),
        migrations.CreateModel(
            name='OfficeBranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_working', models.BooleanField(default=True, help_text='format: required, True=works', verbose_name='Работает ли офис')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефонный номер офиса')),
                ('name', models.CharField(max_length=255, verbose_name='Название офиса')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offices', to='company_structure.address', verbose_name='Адрес офиса')),
                ('departments', models.ManyToManyField(related_name='office', to='company_structure.department', verbose_name='Департаменты/Отделы')),
            ],
            options={
                'verbose_name': 'Филиал',
                'verbose_name_plural': 'Филиалы',
                'unique_together': {('name', 'address')},
            },
        ),
    ]
