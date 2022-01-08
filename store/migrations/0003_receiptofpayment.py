# Generated by Django 4.0 on 2022-01-07 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_is_pay_order_is_confirmed_remove_order_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiptOfPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('cash', 'Наличными'), ('wallet', 'Кошелек'), ('online', 'online')], max_length=16)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('is_canceled', models.BooleanField(default=False)),
                ('create_data', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
        ),
    ]
