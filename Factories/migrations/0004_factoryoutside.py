# Generated by Django 3.2.5 on 2022-01-25 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0001_initial'),
        ('Factories', '0003_remove_factory_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactoryOutSide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ العملية')),
                ('date', models.DateField(null=True, verbose_name='التاريخ')),
                ('number', models.FloatField(blank=True, null=True, verbose_name='الرقم')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='الوزن')),
                ('color', models.CharField(blank=True, max_length=50, null=True, verbose_name='اللون')),
                ('percent_loss', models.FloatField(blank=True, null=True, verbose_name='نسبة الهالك')),
                ('weight_after_loss', models.FloatField(blank=True, null=True, verbose_name='الوزن بعد نسبة الهالك')),
                ('admin', models.CharField(blank=True, max_length=50, null=True, verbose_name='المسئول')),
                ('factory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Factories.factory', verbose_name='المصنع')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.product', verbose_name='المنتج')),
            ],
        ),
    ]
