# Generated by Django 4.2 on 2023-05-17 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purpose',
            name='description',
            field=models.TextField(null=True),
        ),
    ]