# Generated by Django 3.1.1 on 2020-09-22 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_allproduct_imageurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='allproduct',
            name='inStock',
            field=models.BooleanField(default=True),
        ),
    ]
