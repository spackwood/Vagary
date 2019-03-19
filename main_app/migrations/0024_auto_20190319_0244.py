# Generated by Django 2.1.5 on 2019-03-19 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_auto_20190319_0219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='flight',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='hotel',
        ),
        migrations.AddField(
            model_name='flight',
            name='trip',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main_app.Trip'),
            preserve_default=False,
        ),
    ]
