# Generated by Django 2.2.6 on 2020-01-09 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yatranepal', '0009_auto_20200109_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adventuretoplace',
            name='adventure',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='yatranepal.Adventure', verbose_name='Adventure'),
        ),
        migrations.AlterField(
            model_name='adventuretoplace',
            name='place',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='yatranepal.Place', verbose_name='Place Name'),
        ),
        migrations.CreateModel(
            name='PlaceImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placeImage', models.ImageField(upload_to='places/', verbose_name='Image of the Place')),
                ('place', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='yatranepal.Place', verbose_name='Name of the Place')),
            ],
        ),
    ]