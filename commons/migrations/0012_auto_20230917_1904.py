# Generated by Django 3.2.20 on 2023-09-17 22:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('commons', '0011_auto_20230822_2052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('-id',), 'verbose_name': 'Usuário'},
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='shop',
            name='password',
            field=models.CharField(default='', max_length=128),
        ),
    ]
