# Generated by Django 3.0.8 on 2020-07-05 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0007_auto_20200705_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record250',
            name='current_reason_code',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='record250',
            name='previous_reason_code',
            field=models.IntegerField(null=True),
        ),
    ]
