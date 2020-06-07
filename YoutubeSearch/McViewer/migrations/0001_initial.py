# Generated by Django 3.0.6 on 2020-06-07 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_picture', models.ImageField(default='images/default.jpg', upload_to='images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_searched', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.CharField(default='None', max_length=255)),
                ('title', models.CharField(default='None', max_length=255)),
                ('thumbnail', models.ImageField(default='images/default.jpg', upload_to='images')),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='McViewer.UserProfile')),
            ],
        ),
    ]
