# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 21:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jpegmanifesto.web.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MangledImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(height_field='height', upload_to='', width_field='width')),
                ('width', models.PositiveIntegerField(editable=False)),
                ('height', models.PositiveIntegerField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('image', models.ImageField(height_field='height', upload_to=jpegmanifesto.web.models.uploaded_image_path, validators=[jpegmanifesto.web.models.validate_is_jpeg], width_field='width')),
                ('width', models.PositiveIntegerField(editable=False)),
                ('height', models.PositiveIntegerField(editable=False)),
            ],
        ),
        migrations.AddField(
            model_name='mangledimage',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mangled_images', to='web.UploadedImage'),
        ),
    ]
