# Generated by Django 3.2.22 on 2023-11-24 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_order_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
