# Generated by Django 3.2.22 on 2023-10-30 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='on_sale',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
