# Generated by Django 3.2 on 2023-02-23 11:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review_unique_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Минимальная оценка 1'), django.core.validators.MaxValueValidator(10, message='Максимальная оценка 10')], verbose_name='Оценка'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
