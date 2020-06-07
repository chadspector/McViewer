# Generated by Django 3.0.6 on 2020-06-07 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('McViewer', '0002_userprofile_cover_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='thumbnail',
            field=models.ImageField(default='images/default-thumbnail.jpg', upload_to='images'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cover_photo',
            field=models.ImageField(default='images/default-cover.jpg', upload_to='images'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='display_picture',
            field=models.ImageField(default='images/default-display.jpg', upload_to='images'),
        ),
    ]
