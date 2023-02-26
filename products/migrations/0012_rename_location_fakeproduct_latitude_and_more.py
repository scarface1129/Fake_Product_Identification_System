# Generated by Django 4.1.5 on 2023-02-26 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_product_barcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fakeproduct',
            old_name='location',
            new_name='latitude',
        ),
        migrations.AddField(
            model_name='fakeproduct',
            name='longitude',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
