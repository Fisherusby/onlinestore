# Generated by Django 4.2.2 on 2023-07-18 10:33

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('currency', models.CharField(default='BYN', max_length=3, verbose_name='Валюта')),
                (
                    'amount_of_money',
                    models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Количество денег'),
                ),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
