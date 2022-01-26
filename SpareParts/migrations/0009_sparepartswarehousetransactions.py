# Generated by Django 3.2.5 on 2021-12-16 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SpareParts', '0008_auto_20211216_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='SparePartsWarehouseTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0.0, verbose_name='الكمية')),
                ('price_cost', models.FloatField(default=0.0, verbose_name='سعر الشراء')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SpareParts.sparepartsnames', verbose_name='المنتجات')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SpareParts.sparepartswarehouses', verbose_name='المخزن')),
            ],
        ),
    ]
