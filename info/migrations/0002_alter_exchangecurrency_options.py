# Generated by Django 4.0 on 2022-01-07 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exchangecurrency',
            options={'ordering': ['created_date']},
        ),
    ]
