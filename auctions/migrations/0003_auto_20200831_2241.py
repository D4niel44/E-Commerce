# Generated by Django 3.0.3 on 2020-08-31 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200831_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, upload_to='listing_images/<django.db.models.fields.CharField>'),
        ),
    ]