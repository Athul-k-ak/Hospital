# Generated by Django 3.2.25 on 2024-10-06 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20241006_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
