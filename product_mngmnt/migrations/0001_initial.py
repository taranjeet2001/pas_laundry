# Generated by Django 4.2.2 on 2023-06-08 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pName', models.CharField(max_length=50)),
                ('pImage', models.ImageField(upload_to=None)),
                ('pTitle', models.TextField(max_length=250)),
            ],
        ),
    ]
