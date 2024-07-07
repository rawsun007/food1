# Generated by Django 5.0.4 on 2024-07-07 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_alter_savedrecipe_cuisine_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedrecipe',
            name='recipe_image',
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='savedrecipe',
            name='recipe_url',
            field=models.URLField(max_length=2000),
        ),
    ]
