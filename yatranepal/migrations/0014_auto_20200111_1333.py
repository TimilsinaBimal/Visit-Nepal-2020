# Generated by Django 2.2.6 on 2020-01-11 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yatranepal', '0013_adventureimage_hotelimage_packageimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventure',
            name='adventureTheme',
            field=models.CharField(default='', max_length=200, verbose_name='Theme for Adventure'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotelTheme',
            field=models.CharField(default='', max_length=500, verbose_name='Theme of the Hotel'),
        ),
        migrations.AddField(
            model_name='package',
            name='packageTheme',
            field=models.CharField(default='', max_length=500, verbose_name='Theme of the Package'),
        ),
        migrations.AlterField(
            model_name='placeimage',
            name='placeImage',
            field=models.ImageField(upload_to='places/', verbose_name='Images of the Place'),
        ),
    ]
