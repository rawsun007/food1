# Generated by Django 5.0.4 on 2024-05-22 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fastfood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('about', models.TextField(max_length=200)),
                ('img', models.ImageField(upload_to='folder_img')),
            ],
        ),
    ]
