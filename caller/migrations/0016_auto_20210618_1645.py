# Generated by Django 3.2.3 on 2021-06-18 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caller', '0015_table_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='rest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caller.restaurant'),
        ),
        migrations.CreateModel(
            name='Waiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('telegram_id', models.BigIntegerField(verbose_name='Telegram ID')),
                ('rest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caller.restaurant')),
            ],
        ),
    ]
