# Generated by Django 3.2.3 on 2021-06-18 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caller', '0017_auto_20210618_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='n_tables',
        ),
        migrations.AlterField(
            model_name='waiter',
            name='tables',
            field=models.CharField(max_length=100, null=True, verbose_name='Столы'),
        ),
    ]
