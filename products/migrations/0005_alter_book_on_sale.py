# Generated by Django 3.2.22 on 2023-11-27 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_genre_friendly_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='on_sale',
            field=models.BooleanField(default=False),
        ),
    ]