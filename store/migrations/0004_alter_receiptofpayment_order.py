# Generated by Django 4.0 on 2022-01-08 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_receiptofpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiptofpayment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to='store.order'),
        ),
    ]
