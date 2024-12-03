# Generated by Django 5.0.9 on 2024-12-03 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0004_dog_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='dog_name')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth_date')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogs.category', verbose_name='breed')),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogs.dog')),
            ],
            options={
                'verbose_name': 'parent',
                'verbose_name_plural': 'parents',
            },
        ),
    ]
