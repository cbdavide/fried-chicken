# Generated by Django 2.1.7 on 2019-03-04 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='total',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
