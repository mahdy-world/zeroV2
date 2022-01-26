# Generated by Django 3.2.5 on 2021-12-21 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Treasury', '0006_auto_20211214_1623'),
        ('SpareParts', '0016_alter_sparepartsnames_spare_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sparepartsorderoperations',
            name='operation_date',
            field=models.DateTimeField(null=True, verbose_name='تاريخ العملية'),
        ),
        migrations.AlterField(
            model_name='sparepartsorderoperations',
            name='operation_type',
            field=models.IntegerField(choices=[(1, 'دفع عربون'), (2, 'دفع باقي المبلغ'), (3, 'دفع مبلغ تخليص البضاعة'), (4, 'استلام البضاعة'), (5, 'دفع الضرائب')], default=0, verbose_name='نوع العملية'),
        ),
        migrations.AlterField(
            model_name='sparepartsorderoperations',
            name='treasury_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Treasury.worktreasury', verbose_name='الخزنة المستخدمة'),
        ),
    ]
