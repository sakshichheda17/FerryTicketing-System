# Generated by Django 3.0.7 on 2020-09-15 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='passenger_id',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]