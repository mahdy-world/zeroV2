# Generated by Django 3.2.5 on 2022-02-14 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0003_modules'),
    ]

    operations = [
        migrations.AddField(
            model_name='systeminformation',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='شعارالنظام'),
        ),
    ]
