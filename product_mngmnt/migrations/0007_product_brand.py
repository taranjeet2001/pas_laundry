# Generated by Django 4.2.2 on 2023-07-04 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_mngmnt', '0006_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
