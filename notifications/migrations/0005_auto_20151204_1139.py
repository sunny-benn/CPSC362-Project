# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20150826_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='level',
            field=models.CharField(choices=[('success', 'success'), ('info', 'info'), ('warning', 'warning'), ('error', 'error')], default='info', max_length=20),
        ),
    ]
