# Generated by Django 2.0.3 on 2018-11-15 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0003_auto_20181114_1228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='bio',
            new_name='encode',
        ),
    ]