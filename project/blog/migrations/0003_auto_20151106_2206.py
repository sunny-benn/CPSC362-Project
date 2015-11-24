# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20151102_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(max_digits=12, default=0.0, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='listingpicture',
            name='picture',
            field=models.ImageField(null=True, blank=True, upload_to=''),
        ),
    ]
