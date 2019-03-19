# Generated by Django 2.1.5 on 2019-03-19 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_remove_flight_return_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='flight',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main_app.Flight'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trip',
            name='hotel',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main_app.Hotel'),
            preserve_default=False,
        ),
    ]
