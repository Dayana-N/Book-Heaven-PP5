# Generated by Django 3.2.22 on 2023-11-21 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_productreview_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='image',
        ),
    ]
