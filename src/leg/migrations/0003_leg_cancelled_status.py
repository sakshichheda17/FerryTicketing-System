# Generated by Django 3.0.7 on 2020-09-15 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leg', '0002_auto_20200915_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='leg',
            name='cancelled_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
