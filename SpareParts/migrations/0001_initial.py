
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SparePartsNames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='اسم الصنف')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SparePartsSuppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='اسم المورد')),
                ('phone', models.CharField(max_length=11, verbose_name='رقم الهاتف')),
                ('initial_balance', models.FloatField(default=0, verbose_name='الرصيد الافتتاحي')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
            ],
        ),
        migrations.CreateModel(
            name='SparePartsTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='الاسم')),
                ('deleted', models.BooleanField(default=False, verbose_name='مسح')),
            ],
        ),
        migrations.CreateModel(
            name='SparePartsWarehouses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='اسم المخزن')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SparePartsOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=50, null=True, verbose_name='رقم الطلب')),
                ('order_date', models.DateTimeField(null=True, verbose_name='تاريخ الطلب')),
                ('order_deposit_value', models.FloatField(default=0, null=True, verbose_name='قيمة العربون')),
                ('order_deposit_date', models.DateTimeField(null=True, verbose_name='تاريخ دفع العربون')),
                ('order_rest_date', models.DateTimeField(null=True, verbose_name='تاريخ دفع باقي المبلغ')),
                ('order_receipt_date', models.DateTimeField(null=True, verbose_name='تاريخ استلام البضاعة')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
                ('order_supplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SpareParts.sparepartssuppliers', verbose_name='المورد')),
            ],
        ),
        migrations.CreateModel(
            name='SparePartsOrderProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_quantity', models.IntegerField(default=0, null=True, verbose_name='الكمية')),
                ('product_price', models.FloatField(default=0, null=True, verbose_name='سعر الشراء')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
                ('product_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SpareParts.sparepartsnames', verbose_name='المنج')),
                ('product_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SpareParts.sparepartsorders', verbose_name='الطلبية')),
            ],
        ),
    ]
