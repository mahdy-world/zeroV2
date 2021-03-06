# Generated by Django 3.2.5 on 2022-02-24 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0004_auto_20220220_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductWarehouses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='اسم المخزن')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductWarehouseTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0.0, verbose_name='الكمية')),
                ('price_cost', models.FloatField(default=0.0, verbose_name='سعر التكلفة')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Products.product', verbose_name='المنتج')),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Products.productwarehouses', verbose_name='المخزن')),
            ],
        ),
    ]
