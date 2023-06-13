import io
import os
import base64
import datetime
import PIL.Image as Image
from django.db.models.query import Q
from rest_framework import status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Profile, Post, PostImage, Comment, Reply
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import (UserSerializer, RegisterSerializer, LoginSerializer, UpdateProfileDataSerializer, UpdateProfileSerializer, TweetCreateCommentSerializer,
                          TweetCommentSerializer, TweetImageSerializer, TweetReplySerializer, TweetSerializer, TweetCreateSerializer)
import cloudinary.uploader
#Like Tweet 

class LikeTweet(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TweetSerializer
    
    def get(self, request, *args, **kwargs):
        tweetId = kwargs["tweetId"]
        account = self.request.user
        postData = get_object_or_404(Post, pk=tweetId)
        if postData.likes.filter(id=account.pk).exists():
            postData.likes.remove(self.request.user)
            return Response({"like":"unlike"}, status=status.HTTP_200_OK)
        else:
            postData.likes.add(self.request.user)
            return Response({"like":"liked"}, status=status.HTTP_201_CREATED)

    

# # Edit , Delete and get a specific comment

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
                comments = {'comment':data["comment"], 'post':post.pk, 'user':account.pk}
                savecomment = TweetCreateCommentSerializer(data=comments)
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
            return Response({"statusCode": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)

# Update , Delete and view Post

class ViewUpdateDeleteTweet(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = TweetSerializer

    def get(self, request, *args, **kwargs):
        postId = kwargs["pk"]
        postData = Post.objects.get(pk=postId)
        # print(postData.views)
        # postData.views += 1
        # postData.save()
        # print(postData.views)
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

#Get user Tweets

class UserTweets(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = TweetSerializer

    def get(self, request, *args, **kwargs):
        user = kwargs["userId"]
        userDoc = get_object_or_404(User, username=user)
        queryset = self.get_queryset()
        tweets = queryset.filter(user=userDoc.pk)
        serializer = TweetSerializer(tweets, many=True)
        return Response({'tweets': serializer.data}, status=status.HTTP_200_OK)

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
        # print(serializer.data)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)

# All Tweets

class Tweets(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = TweetSerializer

    def get(self, request):
        queryset = Post.objects.all()
        serializer = TweetSerializer(queryset, many=True)
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
        if account != "AnonymousUser":
            return Response({"status": "success", 'follow': userFollow.followers.count(), 'follower': userFollower}, status=status.HTTP_200_OK)
        else:
            userFollowing = Profile.objects.filter(
                user=userDoc, followers=account).exists()
            if userFollowing:
                return Response({"followed": "true", 'follow': userFollow.followers.count(), 'follower': userFollower}, status=status.HTTP_200_OK)
            else:
                return Response({"followed": "false", 'follow': userFollow.followers.count(), 'follower': userFollower}, status=status.HTTP_200_OK)

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
            return Response({"message": "UnFollow Success"                  
                             , "status": "success1", "followed": "true",}, status=status.HTTP_200_OK)
        else:
            userFollow.followers.add(account)
            return Response({"message": "Follow Success", "status": "success2", "followed": "falsess",}, status=status.HTTP_200_OK)

        return Response({"message": "Sorry you cant follow this account", "status": "failed"}, status=status.HTTP_404_NOT_FOUND)

#Update User Profile


class UpdateProfile(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer
    parser_classes = (JSONParser, MultiPartParser)



    def patch(self, request, *args, **kwargs):
        data = request.data
        userInfo = User.objects.get(pk=self.request.user.id)
        userData2 = Profile.objects.get(user=self.request.user)
        user = self.request.user.username
        userExt = f"{self.request.user}.png"
        c = data['image'].split(",")[1]
        b = base64.b64decode(c)
        img = Image.open(io.BytesIO(b))
        img.save(userExt, "PNG")
        response = cloudinary.uploader.upload(userExt, public_id= user, folder=user)
        userExt2 = f"{self.request.user}banner.png"
        c2 = data['bgimage'].split(",")[1]
        b2 = base64.b64decode(c2)
        img2 = Image.open(io.BytesIO(b2))
        img2.save(userExt2, "PNG")
        response2 = cloudinary.uploader.upload(userExt2, public_id= user, folder=f"{user} banner")
        response = cloudinary.uploader.upload(userExt, public_id = user, folder=user)
        prefix = "https://res.cloudinary.com/animecastle/image/upload/"
        userData2.image = response['secure_url'].replace(prefix, "")
        userData2.bgimage = response2['secure_url'].replace(prefix, "")
        userData2.save()
        os.remove(userExt)
        os.remove(userExt2)
        if data['bio'] == '':
            data['bio'] = userData2.bio
            userData2.save()
        
        # print(data['bio'])
        # userData2.bio = data["bio"]
        # userData2.bgimage = data["bgimage"]

        if data['fname'] == '':
            data['fname'] = self.request.user.fname
        if data['lname'] == '':
            data['lname'] = self.request.user.lname
        if data['username'] == '':
            data['username'] = self.request.user.username
        userInfo.fname = data["fname"]
        userInfo.lname = data["lname"]
        if User.objects.filter(pk=self.request.user.pk, username=data["username"]).exists():
            userInfo.username = data["username"]
            userInfo.save()
            return Response({"code":"success"}, status=status.HTTP_200_OK)
        elif User.objects.filter(username=data["username"]).exists():
            return Response({"code":"failed", 'message':"Username is already taken"}, status=status.HTTP_200_OK)
        else:
            userInfo.username = data["username"]
            userInfo.save()



        return Response({'code':'success'}, status=status.HTTP_200_OK)



    # Delete a user account
    def delete(self, request):
        pass

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
        return Response({"message": "Profile page", "status": "success", "data": data}, status=status.HTTP_200_OK)

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
        profil = Profile.objects.get(user=user_data)
        profile = UserSerializer(profil)
        token = RefreshToken.for_user(user_data)
        return Response({"data": serializer.data,"profiledata":profile.data ,"tokenAccess": str(token.access_token), 'tokenRefresh': str(token)}, status=status.HTTP_200_OK)
