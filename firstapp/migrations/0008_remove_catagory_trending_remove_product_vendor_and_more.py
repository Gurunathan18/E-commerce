# Generated by Django 4.1 on 2023-03-24 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0007_remove_catagory_trending_remove_product_vendor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ram',
            field=models.CharField(blank=True, max_length=3),
        )
    ]
