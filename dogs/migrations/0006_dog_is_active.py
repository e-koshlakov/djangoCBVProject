# Generated by Django 5.0.9 on 2024-12-13 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0005_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is_active'),
        ),
    ]
