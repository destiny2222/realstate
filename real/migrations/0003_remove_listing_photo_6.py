# Generated by Django 2.2 on 2022-05-19 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('real', '0002_remove_listing_lot_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='photo_6',
        ),
    ]
