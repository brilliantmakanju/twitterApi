from django.urls import path
from .views import (Register, LoginAPIView, Profiles, Follow,
                    FollowCount, CreateTweet, ViewUpdateDeleteTweet, Tweets)

urlpatterns = [
    path("tweets", Tweets.as_view(), name="tweets"),
    path("login", LoginAPIView.as_view(), name="login"),
    path("register", Register.as_view(), name="register"),
    path("follow/<str:user>", Follow.as_view(), name="follow"),
    path("createtweet", CreateTweet.as_view(), name="createtweet"),
    path("profile/<str:user>", Profiles.as_view(), name="profile"),
    path("followcount/<str:user>", FollowCount.as_view(), name="followcount"),
    path("viewupdatedeletetweet/<int:pk>", ViewUpdateDeleteTweet.as_view(), name="viewupdatedeletetweet"),
]
