# Generated by Django 5.1.1 on 2025-01-09 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeapimodel',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='employee/company_logo/'),
        ),
    ]
