# Generated by Django 4.2.1 on 2023-06-06 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_comment_options_alter_post_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='profileImage'),
        ),
    ]
