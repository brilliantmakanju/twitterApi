from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Profile, Post, PostImage, Comment, Reply


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    create = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Post
        fields = ["update", "comments", 'post', 'create',
                  'tag', 'views', 'user', 'likes', 'pk']


class TweetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["__all__"]


class TweetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["__all__"]


class TweetReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ["__all__"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'image', 'followers']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should only contain alphanumeric chracter")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens', 'pk']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")

        if not user.is_active:
            raise AuthenticationFailed("Account Disabled Contatc the admin")

        print(str(user.tokens))

        return {
            'email': user.email,
            'username': user.username,
            'pk': user.pk,
            'tokens': user.tokens
        }

        return super().validate(attrs)