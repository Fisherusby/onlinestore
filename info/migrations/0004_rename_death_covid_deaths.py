# Generated by Django 4.0 on 2022-01-08 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_covid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='covid',
            old_name='death',
            new_name='deaths',
        ),
    ]
