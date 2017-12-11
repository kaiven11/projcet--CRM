# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 16:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_userprofile_roles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Content', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='客户名称'),
        ),
        migrations.AddField(
            model_name='course',
            name='contract',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Contract'),
        ),
    ]
