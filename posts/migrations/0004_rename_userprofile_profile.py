# Generated by Django 4.2.1 on 2023-05-31 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_userprofile_bio_alter_userprofile_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='Profile',
        ),
    ]
