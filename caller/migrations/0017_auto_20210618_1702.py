# Generated by Django 3.2.3 on 2021-06-18 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caller', '0016_auto_20210618_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='waiter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='caller.waiter'),
        ),
        migrations.AddField(
            model_name='waiter',
            name='tables',
            field=models.CharField(max_length=100, null=True, verbose_name='Столики'),
        ),
    ]
