# Generated by Django 2.0.1 on 2018-01-17 13:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20180111_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='time_start',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 17, 13, 58, 15, 47547, tzinfo=utc)),
        ),
    ]