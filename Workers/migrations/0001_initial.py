# Generated by Django 3.2.5 on 2022-02-21 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='اسم العامل')),
                ('phone', models.IntegerField(null=True, verbose_name='رقم الموبيل')),
                ('worker_type', models.IntegerField(choices=[(1, 'عامل ارضية'), (2, 'عامل خياطة'), (3, 'عامل مكوي'), (4, 'عامل مكينة'), (5, 'عامل عادي')], verbose_name='نوع العامل')),
                ('day_cost', models.FloatField(default=0, null=True, verbose_name='تكلفة اليوم')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
            ],
        ),
    ]