from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from .views import (Register, LoginAPIView, Profiles, Follow,
                    FollowCount, CreateTweet, TweetViewComment, ViewUpdateDeleteTweet, UpdateProfile, UserTweets, LikeTweet, Tweets, TweetComment, AllUsers)

urlpatterns = [
    path("tweets", Tweets.as_view(), name="tweets"),
    path("users", AllUsers.as_view(), name="users"),
    path("login", LoginAPIView.as_view(), name="login"),
    path("register", Register.as_view(), name="register"),
    path("follow/<str:user>", Follow.as_view(), name="follow"),
    path("refresh", TokenRefreshView.as_view(), name="refresh"),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("createtweet", CreateTweet.as_view(), name="createtweet"),
    path("profile/<str:user>", Profiles.as_view(), name="profile"),
    path("like/<int:tweetId>", LikeTweet.as_view(), name="liketweet"),
    path("updateprofile", UpdateProfile.as_view(), name="updateprofile"),
    path("usertweets/<str:userId>", UserTweets.as_view(), name="usertweets"),
    path("followcount/<str:user>", FollowCount.as_view(), name="followcount"),
    path("comment/createview/<int:postId>", TweetComment.as_view(), name="createcomment"),
    path("viewupdatedeletecomments/<int:pk>", TweetViewComment.as_view(), name="viewupdatedeletecomment"),
    path("viewupdatedeletetweet/<int:pk>", ViewUpdateDeleteTweet.as_view(), name="viewupdatedeletetweet"),
]
