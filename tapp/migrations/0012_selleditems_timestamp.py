# Generated by Django 4.2.15 on 2024-12-13 11:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tapp', '0011_rename_name_selleditems_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='selleditems',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
