# Generated by Django 4.0.6 on 2022-08-04 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan_system', '0002_loanlimitamounthistory_loanlimitamount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('A', 'Рекомендации системы'), ('CI', 'Информация для консультации')], max_length=10, unique=True, verbose_name='Название информации')),
                ('text', models.TextField(verbose_name='Текст информации')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
            ],
            options={
                'verbose_name': 'Информация',
                'verbose_name_plural': 'Информации',
                'ordering': ('-created_date',),
            },
        ),
    ]
