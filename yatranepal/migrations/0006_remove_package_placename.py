# Generated by Django 2.2.6 on 2020-01-06 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yatranepal', '0005_auto_20200106_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='placeName',
        ),
    ]
