from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Profile

# def Register(request):
#     if request.method == "POST":
#         user = request.data

#         serializers = RegisterSerializer(data=user)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()

#         user_data = serializers.data
#         return Response(user_data, status=status.HTTP_201_CREATED)


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
            userFollowing = Profile.objects.filter(user=userDoc, followers=account).exists()
            if userFollowing:
                return Response({"followed":"true", 'follow': userFollow.followers.count(), 'follower': userFollower}, status=status.HTTP_200_OK) 
            else:
                return Response({"followed":"false", 'follow': userFollow.followers.count(), 'follower': userFollower}, status=status.HTTP_200_OK) 
                
        return Response({"status": "success", 'follow': userFollow.followers.count(), 'follower': userFollower}, status=status.HTTP_404_NOT_FOUND)


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
        # userFollower = get_object_or_404(Profile, followers=userDoc)
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
