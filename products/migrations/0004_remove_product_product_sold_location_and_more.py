# Generated by Django 4.1.5 on 2023-02-10 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_sold_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_sold_location',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sold_date',
        ),
    ]
