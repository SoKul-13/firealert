# Generated by Django 3.0.8 on 2021-01-18 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firealert', '0002_auto_20210118_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irwindata',
            name='city',
            field=models.CharField(max_length=30, null=True),
        ),
    ]