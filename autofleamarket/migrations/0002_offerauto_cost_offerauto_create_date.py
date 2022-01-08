# Generated by Django 4.0 on 2022-01-07 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autofleamarket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerauto',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='offerauto',
            name='create_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]