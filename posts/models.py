from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("Users should have a username")
        if email is None:
            raise TypeError("Users should have a Email")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError("Password should not be null")
        if email is None:
            raise TypeError("Users should have a Email")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    fname = models.CharField(max_length=255, null=False, blank=False, default="")
    lname = models.CharField(max_length=255, null=False, blank=False, default="")
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),

        }


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="Welcome to my Profile", blank=True)
    followers = models.ManyToManyField(
        User, blank=True, related_name="followed")
    bgimage =  models.ImageField(upload_to='profileBanner', default="/profile/bgImage.jpg")
    image = models.ImageField(upload_to='profileImage', default="/profile/Default.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return str(self.user.fname)



# Model for Tweets
class Post(models.Model):
    update = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    post = models.TextField(blank=False, null=False)
    create = models.DateTimeField(auto_now_add=True)
    tag = models.TextField(blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="postlikes")
    retweet = models.ManyToManyField('Retweet', verbose_name='tweetRetweets', blank=True, related_name='tweetRetweet')
    comments = models.ManyToManyField("Comment", verbose_name="tweetComments", blank=True , related_name="tweetComment")

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return str(self.user)

#Model for Retweet
class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tweetRetweetst')

    class Meta:
            ordering = ["-pk"]

    def __str__(self):
        return str(self.tweet)

# Model for Tweet Images
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post/image", blank=True)
    # image = models

    def __str__(self):
        return str(self.post.user)

# Model for COmments on Tweet


class Comment(models.Model):
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(default="Create Comment")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    likes = models.ManyToManyField(
        User, blank=True, related_name="commentlikes")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="tweetCommenst")

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return str(self.post.user)
    

# MOdel for reply


class Reply(models.Model):
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(default="Create Reply")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="replylikes")

    def __str__(self):
        return str(self.comment.post.user)
