# Generated by Django 3.2.3 on 2021-06-14 05:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_rest_', '0025_auto_20210614_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_table',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 14, 10, 20, 20, 957986)),
        ),
        migrations.AlterField(
            model_name='sold',
            name='data_buy',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 14, 10, 20, 20, 956988)),
        ),
    ]
