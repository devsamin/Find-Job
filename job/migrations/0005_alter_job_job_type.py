# Generated by Django 5.1.1 on 2025-01-31 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_alter_job_job_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(blank=True, choices=[('FullTime', 'FullTime'), ('PartTime', 'PartTime'), ('Internship', 'Internship')], default='PartTime', max_length=20, null=True),
        ),
    ]
