# Generated by Django 2.2 on 2021-12-17 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20211217_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='vote',
            field=models.IntegerField(default=0),
        ),
    ]
