# Generated by Django 3.2.5 on 2022-03-08 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Workers', '0002_workerattendance_workerpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='صورة العامل'),
        ),
    ]
