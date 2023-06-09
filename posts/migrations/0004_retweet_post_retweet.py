# Generated by Django 4.2.1 on 2023-06-04 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tweetRetweetst', to='posts.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.AddField(
            model_name='post',
            name='retweet',
            field=models.ManyToManyField(blank=True, related_name='tweetRetweet', to='posts.retweet', verbose_name='tweetRetweets'),
        ),
    ]
