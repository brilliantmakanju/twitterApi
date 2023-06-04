import datetime
from rest_framework import status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Profile, Post, PostImage, Comment, Reply
from .serializers import (UserSerializer, RegisterSerializer, LoginSerializer,
                          TweetCommentSerializer, TweetImageSerializer, TweetReplySerializer, TweetSerializer, TweetCreateSerializer)


# Edit , Delete and get a specific comment

class TweetViewComment(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = TweetCommentSerializer

    def get(self, request, *args, **kwargs):
        # Get Sinlge Comments
        
        pass

    def patch(self, request, *args, **kwargs):
        # Update Comment
        pass

    def delete(self, request, *args, **kwargs):
        # Delete COmment
        pass


# Get all Tweet Comment and Create Comment


class TweetComment(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = TweetCommentSerializer

    def get(self, request, *args, **kwargs):
        # Get all comment for a single post
        postId = kwargs["postId"]
        try:
            post = Post.objects.get(pk=postId)
            comment = Comment.objects.filter(post=post)
            comments = TweetCommentSerializer(comment, many=True)
            return Response({"status":"success", 'comments':comments.data}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"status":"failed", "message":"Post Does not Exists"}, status=status.HTTP_404_NOT_FOUND)



    def post(self, request, *args, **kwargs):
        # Create new Comment
        data = request.data
        postId = kwargs["postId"]
        account = self.request.user
        try:
            post = Post.objects.get(pk=postId)
            if account:
                comments = {'comment':data['comment'], 'post':post.pk, 'user':account.pk}
                savecomment = self.serializer_class(data=comments)
                savecomment.is_valid(raise_exception=True)
                savecomment.save()
                post.comments.add(savecomment.data['id'])
                return Response({"status":"success"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status":"failed", "message":"Y0u need to be logged in to comment"}, status=status.HTTP_401_UNAUTHORIZED)
        except Post.DoesNotExist:
            return Response({"status":"failed", "message":"Post Does not Exists"}, status=status.HTTP_404_NOT_FOUND)



# Create Tweets


class CreateTweet(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TweetCreateSerializer

    def post(self, request):
        postdata = request.data
        user = self.request.user
        date = datetime.datetime.now()
        # print(user.pk)
        postdata = {'post': postdata['post'],
                    'tag': postdata['tag'], 'user': user.pk, 'create':date.strftime('%Y-%m-%d %H:%M:%S')}
        # print(postdata)
        posts = self.serializer_class(data=postdata)
        if posts.is_valid():
            posts.save()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)


# Update , Delete and view Post
class ViewUpdateDeleteTweet(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = TweetSerializer

    def get(self, request, *args, **kwargs):
        postId = kwargs["pk"]
        postData = Post.objects.get(pk=postId)
        serializer = TweetSerializer(postData)
        comment = Comment.objects.filter(post=postData)
        comments = TweetCommentSerializer(comment, many=True)
        return Response({"tweet": serializer.data, "comments":comments.data}, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        postId = kwargs["pk"]
        try:
            postData = Post.objects.get(pk=postId)
            if postData.user.pk == self.request.user.pk:
                postdata = request.data
                user = self.request.user
                postdata = {'post': postdata['post'],
                            'tag': postdata['tag'], 'user': user.pk}
                posts = self.serializer_class(postData, data=postdata)
                posts.is_valid(raise_exception=True)
                posts.save()
                return Response({"status": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "failed", "message": "Cant Edit Tweet you did not create"}, status=status.HTTP_404_NOT_FOUND)

        except Post.DoesNotExist:
            return Response({"status": "failed"}, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        postId = kwargs["pk"]
        try:
            postData = Post.objects.get(pk=postId)
            if postData.user.pk == self.request.user.pk:
                postData.delete()
                return Response({"status": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "failed", "message": "Cant Delete Tweet you did not Create"}, status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response({"status": "failed"}, status=status.HTTP_204_NO_CONTENT)


#Get all user thats not being followed
class AllUsers(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        user = self.request.user
        queryset = self.get_queryset()
        users = queryset.exclude(user=user)
        serializer = UserSerializer(users, many=True)
        print(serializer.data)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)



# All Tweets


class Tweets(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = TweetSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = TweetSerializer(queryset, many=True)
        # comment = Comment.objects.filter(post=17)
        # print(serializer.data.comments.count())
        return Response({'tweets': serializer.data}, status=status.HTTP_200_OK)

# Count Followers and Following


class FollowCount(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, **kwargs):
        user = kwargs['user']
        account = self.request.user
        userDoc = get_object_or_404(User, username=user)
        userFollow = get_object_or_404(Profile, user=userDoc)
        userFollower = Profile.objects.filter(followers=userDoc).count()
        if account:
            userFollowing = Profile.objects.filter(
                user=userDoc, followers=account).exists()
            if userFollowing:
                return Response({"followed": "true", 'follow': userFollow.followers.count(), 'follower': userFollower}, status=status.HTTP_200_OK)
            else:
                return Response({"followed": "false", 'follow': userFollow.followers.count(), 'follower': userFollower}, status=status.HTTP_200_OK)

        return Response({"status": "success", 'follow': userFollow.followers.count(), 'follower': userFollower}, status=status.HTTP_404_NOT_FOUND)

# Follow FUnctionanilty


class Follow(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, **kwargs):
        user = kwargs['user']
        account = self.request.user
        userDoc = get_object_or_404(User, username=user)
        userFollow = get_object_or_404(Profile, user=userDoc)
        if userFollow.followers.filter(id=account.pk).exists():
            userFollow.followers.remove(account)
            return Response({"message": "UnFollow Success"                             # userFollower = get_object_or_404(Profile, followers=userDoc)
                             # if userFollower:
                             #     follow = userFollow.followers.count()
                             #     print(follow)


                             # follower = userFollower.count()
                             # print(follower)
                             # followerId = Profile.objects.get(user=)
                             , "status": "success1"}, status=status.HTTP_200_OK)
        else:
            userFollow.followers.add(account)
            return Response({"message": "Follow Success", "status": "success2"}, status=status.HTTP_200_OK)

        return Response({"message": "Sorry you cant follow this account", "status": "failed"}, status=status.HTTP_404_NOT_FOUND)

# USer Profile


class Profiles(generics.GenericAPIView):

    serializer_class = UserSerializer

    # Get user inFormation for a profile page
    def get(self, request, *args, **kwargs):
        userId = kwargs["user"]
        userDoc = get_object_or_404(User, username=userId)
        try:
            userdata = Profile.objects.get(user=userDoc)
        except Profile.DoesNotExist:
            return Response({"message": "Profile for this account does not exist", "status": "failed"}, status=status.HTTP_404_NOT_FOUND)
        userInfo = self.get_serializer(userdata)
        data = userInfo.data
        # user = [user for user in userdata.followers.all()]
        # user = Profile.objects.get(followers=)
        # print(user)

        return Response({"message": "Profile page", "status": "success", "data": data}, status=status.HTTP_200_OK)

    # Update user information for a profile
    def post(self, request):
        pass

    # Delete a user account
    def delete(self, request):
        pass


class Register(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user)

        return Response({"message": "User Created "}, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user_data = User.objects.get(email=serializer.data['email'])
        token = RefreshToken.for_user(user_data)
        return Response({"data": serializer.data, "tokenAccess": str(token.access_token), 'tokenRefresh': str(token)}, status=status.HTTP_200_OK)
