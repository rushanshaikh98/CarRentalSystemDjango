# Generated by Django 4.2.5 on 2023-10-05 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_remove_car_car_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='number_plate',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
