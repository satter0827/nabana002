# Generated by Django 3.0.7 on 2020-07-02 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='uuid',
            new_name='id',
        ),
    ]