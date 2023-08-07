# Generated by Django 3.2.18 on 2023-08-01 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0013_auto_20230731_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('subject', models.TextField()),
                ('message', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='newsletter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='checkout',
            name='orderstatus',
            field=models.IntegerField(choices=[(0, 'Order is Placed'), (1, 'Order is Packed'), (2, 'Ready to Dispatch'), (3, 'Dispatched'), (4, 'Out For Delivery'), (5, 'Delivered')], default=0),
        ),
    ]
