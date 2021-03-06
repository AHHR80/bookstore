# Generated by Django 3.2.3 on 2021-06-06 15:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_rest_', '0010_auto_20210606_1649'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book_table',
            old_name='counter',
            new_name='counter_opi',
        ),
        migrations.AddField(
            model_name='book_table',
            name='counter_star',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='book_table',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 6, 19, 44, 11, 208058)),
        ),
        migrations.AlterField(
            model_name='sold',
            name='data_buy',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 6, 19, 44, 11, 205059)),
        ),
    ]
