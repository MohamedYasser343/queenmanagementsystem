# Generated by Django 4.2.15 on 2024-08-19 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
