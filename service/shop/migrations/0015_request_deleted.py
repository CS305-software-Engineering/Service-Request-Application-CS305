# Generated by Django 3.1.7 on 2021-05-04 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20210503_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='deleted',
            field=models.IntegerField(default=-1),
        ),
    ]
