# Generated by Django 3.2.18 on 2023-08-02 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0018_auto_20230802_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='latitude',
            field=models.TextField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='longitude',
            field=models.TextField(max_length=50),
        ),
    ]