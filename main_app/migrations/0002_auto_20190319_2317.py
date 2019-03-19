# Generated by Django 2.1.5 on 2019-03-19 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='price_currency',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='price_currency',
        ),
        migrations.AlterField(
            model_name='flight',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='price',
            field=models.FloatField(),
        ),
    ]
