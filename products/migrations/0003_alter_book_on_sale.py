# Generated by Django 3.2.22 on 2023-10-30 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_book_on_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='on_sale',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]