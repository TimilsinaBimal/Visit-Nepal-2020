# Generated by Django 2.2.6 on 2020-01-05 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adventures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adventureName', models.CharField(max_length=200)),
                ('adventureDesc', models.TextField()),
                ('adventureImage', models.ImageField(upload_to='adventures/')),
                ('adventureSlug', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Hotels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotelName', models.CharField(max_length=255)),
                ('hotelAddress', models.CharField(max_length=255)),
                ('hotelImage', models.ImageField(upload_to='hotels/')),
                ('hotelDesc', models.TextField()),
                ('hotelFeatures', models.TextField()),
                ('hotelPrice', models.IntegerField()),
                ('hotelSlug', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placeName', models.CharField(max_length=255)),
                ('placeImage', models.ImageField(upload_to='places/')),
                ('placeDesc', models.TextField()),
                ('placeSlug', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TransportationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transportationType', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Transportation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placeFrom', models.CharField(max_length=200)),
                ('placeTo', models.CharField(max_length=200)),
                ('fare', models.IntegerField()),
                ('transportationType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yatranepal.TransportationType')),
            ],
        ),
    ]
