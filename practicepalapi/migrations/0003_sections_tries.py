# Generated by Django 3.1.7 on 2021-03-09 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practicepalapi', '0002_auto_20210309_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='sections',
            name='tries',
            field=models.IntegerField(default=3),
        ),
    ]
