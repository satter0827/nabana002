# Generated by Django 3.0.7 on 2020-07-02 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200702_2358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='id',
            new_name='uuid',
        ),
    ]
