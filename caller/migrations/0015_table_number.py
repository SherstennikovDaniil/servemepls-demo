# Generated by Django 3.2.3 on 2021-06-18 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caller', '0014_auto_20210618_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='number',
            field=models.IntegerField(default=1, verbose_name='Номер стола'),
        ),
    ]
