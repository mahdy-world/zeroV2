# Generated by Django 3.2.5 on 2022-01-21 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_alter_systeminformation_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_active', models.BooleanField(default=True, verbose_name='تنشيط المكينات')),
                ('spareParts_active', models.BooleanField(default=True, verbose_name='تنشيط قطع الغيار')),
                ('treasurty_active', models.BooleanField(default=True, verbose_name='تنشيط الخزينة')),
                ('factory_active', models.BooleanField(default=True, verbose_name='تنشيط المصانع')),
                ('products_active', models.BooleanField(default=True, verbose_name='تنشيط المنتجات')),
                ('wools_active', models.BooleanField(default=True, verbose_name='تنشيط مخازن الصوف ')),
            ],
        ),
    ]
