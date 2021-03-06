# Generated by Django 2.2.6 on 2020-01-23 08:48

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        ('yatranepal', '0021_auto_20200123_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='name',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
