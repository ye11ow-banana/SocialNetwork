# Generated by Django 4.2 on 2023-04-24 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_alter_postlike_date_created'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='postlike',
            table='post_like',
        ),
    ]
