# Generated by Django 4.2 on 2023-04-22 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='title',
        ),
    ]
