# Generated by Django 3.2.20 on 2023-08-06 23:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('commons', '0003_tracking_finished'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tracking',
            name='finished',
        ),
        migrations.AddField(
            model_name='sale',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
