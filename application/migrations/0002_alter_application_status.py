# Generated by Django 5.1.1 on 2025-01-11 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('Applied', 'Applied'), ('Under Review', 'Under Review'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Applied', max_length=40),
        ),
    ]
