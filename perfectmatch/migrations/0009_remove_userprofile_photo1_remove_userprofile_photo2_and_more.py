# Generated by Django 4.1.6 on 2023-02-06 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfectmatch', '0008_alter_userprofile_photo1_alter_userprofile_photo2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='photo1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='photo2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='photo3',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='photo4',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='photo5',
        ),
    ]
