# Generated by Django 4.2.15 on 2024-08-19 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypp', '0003_name_alter_entry_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='name',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
