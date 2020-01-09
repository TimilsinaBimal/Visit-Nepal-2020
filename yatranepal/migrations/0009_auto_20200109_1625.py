# Generated by Django 2.2.6 on 2020-01-09 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yatranepal', '0008_adventuretoplace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adventuretoplace',
            name='adventure',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='yatranepal.Adventure', verbose_name='Places for this Adventure'),
        ),
        migrations.AlterField(
            model_name='adventuretoplace',
            name='place',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='yatranepal.Place', verbose_name='Adventures in this Place'),
        ),
    ]
