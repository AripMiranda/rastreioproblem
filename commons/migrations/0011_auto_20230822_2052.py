# Generated by Django 3.2.20 on 2023-08-22 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0010_auto_20230822_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='rg',
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]