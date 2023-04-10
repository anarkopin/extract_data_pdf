# Generated by Django 3.2.16 on 2023-04-10 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaxFiling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador', models.CharField(max_length=255)),
                ('tax_filing', models.CharField(max_length=255)),
                ('wages', models.IntegerField()),
                ('total_deductions', models.IntegerField()),
            ],
        ),
    ]
