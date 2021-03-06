# Generated by Django 3.0.6 on 2020-06-13 03:51

import ckeditor_uploader.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('serialnumber', models.AutoField(primary_key=True, serialize=False)),
                ('blogtitle', models.CharField(max_length=255)),
                ('Thumbnail_image', models.ImageField(blank=True, upload_to='home/images/blog_thumbnail_images')),
                ('blog_des', models.CharField(blank=True, max_length=500)),
                ('blogcontent', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('writer', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=200)),
                ('time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
    ]
