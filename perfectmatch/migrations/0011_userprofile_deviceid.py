# Generated by Django 4.1.6 on 2023-02-08 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfectmatch', '0010_userprofile_photo1_userprofile_photo2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='deviceid',
            field=models.TextField(null=True),
        ),
    ]
