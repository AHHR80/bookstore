# Generated by Django 3.2.3 on 2021-06-13 08:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_rest_', '0020_auto_20210613_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_table',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 13, 12, 40, 13, 553678)),
        ),
        migrations.AlterField(
            model_name='sold',
            name='data_buy',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 13, 12, 40, 13, 552678)),
        ),
    ]
