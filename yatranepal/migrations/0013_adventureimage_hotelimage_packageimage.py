# Generated by Django 2.2.6 on 2020-01-10 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yatranepal', '0012_auto_20200110_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('packageImages', models.ImageField(upload_to='packages/', verbose_name='Image of the Package')),
                ('package', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='yatranepal.Package', verbose_name='Name of the package')),
            ],
        ),
        migrations.CreateModel(
            name='HotelImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotelImages', models.ImageField(upload_to='hotels/', verbose_name='Image of the Hotel')),
                ('hotel', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='yatranepal.Hotel', verbose_name='Name of the Hotel')),
            ],
        ),
        migrations.CreateModel(
            name='AdventureImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adventureImages', models.ImageField(upload_to='adventures/', verbose_name='Image of the adventure')),
                ('adventure', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='yatranepal.Adventure', verbose_name='Name of the Adventure')),
            ],
        ),
    ]