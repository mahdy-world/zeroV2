# Generated by Django 3.2.5 on 2022-02-25 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0005_productwarehouses_productwarehousetransactions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productwarehousetransactions',
            name='price_cost',
        ),
    ]
