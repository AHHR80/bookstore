# Generated by Django 3.2.3 on 2021-06-06 12:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_rest_', '0009_auto_20210606_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_table',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 6, 16, 49, 30, 42280)),
        ),
        migrations.AlterField(
            model_name='sold',
            name='data_buy',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 6, 16, 49, 30, 40279)),
        ),
    ]
