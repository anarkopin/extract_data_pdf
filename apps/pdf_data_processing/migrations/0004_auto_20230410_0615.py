# Generated by Django 3.2.16 on 2023-04-10 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_data_processing', '0003_auto_20230410_0530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltaxfiling',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='taxfiling',
            name='created_by',
        ),
    ]
