# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20151106_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingpicture',
            name='picture',
            field=models.ImageField(upload_to=''),
        ),
    ]
