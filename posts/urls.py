from django.urls import path
from .views import Register, LoginAPIView, Profiles, Follow, FollowCount

urlpatterns = [
    path("login", LoginAPIView.as_view(), name="login"),
    path("register", Register.as_view(), name="register"),
    path("follow/<str:user>", Follow.as_view(), name="follow"),
    path("profile/<str:user>", Profiles.as_view(), name="profile"),
    path("followcount/<str:user>", FollowCount.as_view(), name="followcount"),
]
