# Generated by Django 3.0.8 on 2021-01-19 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firealert', '0005_zipdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zipdata',
            name='zip',
            field=models.IntegerField(unique=True),
        ),
    ]