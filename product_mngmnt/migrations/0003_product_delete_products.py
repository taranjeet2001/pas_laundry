# Generated by Django 4.2.2 on 2023-06-15 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_mngmnt', '0002_rename_pimage_products_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to=None)),
                ('description', models.TextField(max_length=250)),
            ],
        ),
        migrations.DeleteModel(
            name='Products',
        ),
    ]
