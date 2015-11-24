# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListingPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('picture', models.ImageField(upload_to='blog/picture_uploads')),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, default=0.0),
        ),
        migrations.AddField(
            model_name='listingpicture',
            name='picture_id',
            field=models.ForeignKey(to='blog.Listing'),
        ),
    ]
