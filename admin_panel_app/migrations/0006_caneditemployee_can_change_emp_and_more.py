# Generated by Django 4.2.6 on 2023-12-06 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel_app', '0005_caneditemployee'),
    ]

    operations = [
        migrations.AddField(
            model_name='caneditemployee',
            name='can_change_emp',
            field=models.BooleanField(default=False, null=True, verbose_name='Редактировать данные сотрудников'),
        ),
        migrations.AddField(
            model_name='caneditemployee',
            name='can_change_rules',
            field=models.BooleanField(default=False, null=True, verbose_name='Назначать права сотрудников'),
        ),
        migrations.AddField(
            model_name='caneditemployee',
            name='can_upload',
            field=models.BooleanField(default=False, null=True, verbose_name='Делать выгрузки списков'),
        ),
    ]
