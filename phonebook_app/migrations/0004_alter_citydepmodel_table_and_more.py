# Generated by Django 4.2.6 on 2023-11-24 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook_app', '0003_alter_citydepmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='citydepmodel',
            table='admin_panel_app_citydepmodel',
        ),
        migrations.AlterModelTable(
            name='moredetailsemployeemodel',
            table='admin_panel_app_moredetailsemployeemodel',
        ),
    ]
