# Generated by Django 5.0.4 on 2024-07-07 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0008_rename_saved_recipes_userprofile_saved_recipes_fastfood_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='saved_recipes_fastfood',
        ),
    ]
