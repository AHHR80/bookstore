# Generated by Django 3.2.3 on 2021-06-09 05:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_rest_', '0012_auto_20210607_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='shop_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.IntegerField(default=0)),
                ('book_name', models.CharField(max_length=150)),
                ('user', models.CharField(default='amir', max_length=150)),
                ('price', models.CharField(default='0', max_length=15)),
            ],
        ),
        migrations.AlterField(
            model_name='book_table',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 9, 10, 5, 22, 207491)),
        ),
        migrations.AlterField(
            model_name='sold',
            name='data_buy',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 9, 10, 5, 22, 205492)),
        ),
    ]