# Generated by Django 4.2.1 on 2023-06-08 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_alter_profile_bgimage_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bgimage',
            field=models.ImageField(upload_to='', verbose_name='profileBanner'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='profileImage'),
        ),
    ]