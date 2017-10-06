# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-06 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0002_transporter_contact_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='approval_status',
            field=models.CharField(choices=[('approved', 'approved'), ('unapproved', 'unapproved'), ('rejected', 'rejected')], default='unapproved', max_length=120),
        ),
        migrations.AlterField(
            model_name='transporter',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], max_length=120),
        ),
    ]
