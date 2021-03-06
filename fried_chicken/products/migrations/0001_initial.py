# Generated by Django 2.1.7 on 2019-03-03 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_date', models.DateField()),
                ('input_amount', models.PositiveSmallIntegerField()),
                ('current_amount', models.PositiveSmallIntegerField()),
                ('out_of_stock_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('unity', models.CharField(max_length=20)),
                ('price_per_unity', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='inventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='inventory',
            order_with_respect_to='input_date',
        ),
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together={('input_date', 'product')},
        ),
    ]
