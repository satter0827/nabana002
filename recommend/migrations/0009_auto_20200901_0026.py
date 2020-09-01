# Generated by Django 3.0.7 on 2020-08-31 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0008_resultknn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='anime_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='anime',
            name='genre',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='anime',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user_id',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='result',
            name='user_id',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='resultknn',
            name='user_id',
            field=models.CharField(max_length=200),
        ),
    ]