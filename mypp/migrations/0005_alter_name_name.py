# Generated by Django 4.2.15 on 2024-08-19 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypp', '0004_alter_name_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='name',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
