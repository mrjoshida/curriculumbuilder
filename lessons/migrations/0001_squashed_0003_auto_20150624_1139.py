# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    replaces = [('lessons', '0001_initial'), ('lessons', '0002_auto_20150623_2105'), ('lessons', '0003_auto_20150624_1139')]

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('standards', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('name', models.CharField(max_length=255)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name=b'Activity Content')),
                ('ancestor', models.ForeignKey(blank=True, to='lessons.Activity', null=True)),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name_plural': 'activities',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('overview', mezzanine.core.fields.RichTextField(verbose_name=b'Lesson Overview')),
                ('duration', models.IntegerField(verbose_name=b'Class Periods')),
                ('unplugged', models.BooleanField(default=False)),
                ('resources', mezzanine.core.fields.RichTextField(null=True, blank=True)),
                ('ancestor', models.ForeignKey(blank=True, to='lessons.Lesson', null=True)),
                ('anchor_standards', models.ManyToManyField(related_name='anchors', to=b'standards.Standard')),
                ('standards', models.ManyToManyField(to=b'standards.Standard')),
            ],
            options={
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('lesson', models.ForeignKey(to='lessons.Lesson')),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.CreateModel(
            name='Prereq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('lesson', models.ForeignKey(to='lessons.Lesson')),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='lesson',
            field=models.ForeignKey(to='lessons.Lesson'),
        ),
        migrations.CreateModel(
            name='Vocab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=255)),
                ('simpleDef', models.TextField()),
                ('detailDef', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='vocab',
            field=models.ManyToManyField(to=b'lessons.Vocab', blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='anchor_standards',
            field=models.ManyToManyField(related_name='anchors', to=b'standards.Standard', blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='standards',
            field=models.ManyToManyField(to=b'standards.Standard', blank=True),
        ),
    ]
