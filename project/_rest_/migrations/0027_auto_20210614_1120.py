# Generated by Django 3.2.3 on 2021-06-14 06:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_rest_', '0026_auto_20210614_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_table',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 14, 11, 20, 48, 107880)),
        ),
        migrations.AlterField(
            model_name='sold',
            name='data_buy',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 14, 11, 20, 48, 105883)),
        ),
    ]