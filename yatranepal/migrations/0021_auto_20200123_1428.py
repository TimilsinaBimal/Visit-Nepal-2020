# Generated by Django 2.2.6 on 2020-01-23 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yatranepal', '0020_auto_20200123_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='name',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
