# Generated by Django 3.2.20 on 2023-08-11 20:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('commons', '0008_shop_url_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
