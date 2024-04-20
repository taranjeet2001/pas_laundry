# Generated by Django 4.2.3 on 2023-07-07 04:36

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_mngmnt', '0009_alter_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AddField(
            model_name='product',
            name='detail',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]