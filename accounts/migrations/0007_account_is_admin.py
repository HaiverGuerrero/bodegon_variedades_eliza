# Generated by Django 3.1 on 2023-07-17 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20230717_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
