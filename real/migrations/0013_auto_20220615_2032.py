# Generated by Django 2.2 on 2022-06-15 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real', '0012_alter_customuser_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]