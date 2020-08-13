# Generated by Django 3.0.7 on 2020-07-08 15:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0005_auto_20200709_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='evaluation',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
