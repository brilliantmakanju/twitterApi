from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Profile, Post, PostImage, Comment, Reply

# class UpdatePassword(serializers.ModelSerializer):
#     old_password = serializers.CharField(write_only=True, required=True)
#     new_password_confirm = serializers.CharField(write_only=True, required=True)
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

#     class Meta:
#         model = User
#         fields = ('old_password','new_password_confirm', 'password')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['new_password_confirm']:
#             raise serializers.ValidationError({"password":"Password fields did'n match"})
#         return attrs
    
#     def validate_old_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError({"old_password":"Old password is not correct"})
        
#     def update(self, instance, validate_data):
#         instance.set_password(validate_data['password'])
#         instance.save()

#         return instance


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.user.username")
    userimage = serializers.CharField(source="user.image")
    create = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    userfname = serializers.CharField(source="user.user.fname")
    userlname = serializers.CharField(source="user.user.lname")
    class Meta:
        model = Post
        fields = ["update", 'retweet', "comments", 'post', 'create',
                  'tag', 'views', 'user', 'likes', 'pk', 'userimage', 'userfname','userlname']

class TweetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["update", 'retweet', "comments", 'post', 'create',
                  'tag', 'views', 'user', 'likes', 'pk']




class TweetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["__all__"]

class TweetCreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("__all__")

class TweetCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    userimage = serializers.CharField(source="user.image")
    userfname = serializers.CharField(source="user.user.fname")
    userlname = serializers.CharField(source="user.user.lname")
    class Meta:
        model = Comment
        fields = ("__all__")


class TweetReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ["__all__"]

class UpdateProfileDataSerializer(serializers.Serializer):
    image = serializers.ImageField(use_url=True, max_length=None)

    class Meta:
        model = Profile
        fields = ("bio", 'image', 'bgimage')

class UpdateProfileSerializer(serializers.Serializer):
    fname = serializers.CharField(required=True)
    lname = serializers.CharField(required=True)
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context['request'].user
        email = attrs.get('email', '')
        fname = attrs.get('fname', '')
        lname = attrs.get('lname', 's')
        username = attrs.get('username', '')
        # if User.objects.exclude(pk=user.pk).filter(email=email).exists():
        #     raise serializers.ValidationError("This email is already taken")
        if User.objects.exclude(pk=user.pk).filter(username=username).exists():
            raise serializers.ValidationError("This Username is already taken")
        return attrs
    
    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


# class UpdateProfileSerializer(serializers.Serializer):
#     # profileBio = UpdateProfileDataSerializer(source="userprofile", many=False)
    
#     fname = serializers.CharField()
#     lname = serializers.CharField()
#     email = serializers.EmailField(read_only=True)
#     username = serializers.CharField()


#     # class Meta:
#     #     model = User
#     #     fields = ['fname', 'lnme', 'username', 'email']
#     #     extra_kwargs = {
#     #         'fname':{'required':True},
#     #         'lname':{'required':True},
#     #     }

#     def validate_email(self, value):
#         user = self.context['request'].user
#         if User.objects.exclude(pk=user.pk).filter(email=value).exists():
#             raise serializers.ValidationError({"email":"This email is already taken"})
#         return value
    
#     def validate_username(self, value):
#         user = self.context['request'].user
#         if User.objects.exclude(pk=user.pk).filter(username=value).exists():
#             raise serializers.ValidationError({"username":"This username is already taken"})
#         return value
    
#     def update(self, instance, validated_data):
#         # user = self.context['request'].user
#         # if user.pk != instance.pk:
#         #     raise serializers.ValidationError({"authorize":"You don't have permission for this user"})
#         # instance.fname = validated_data['fname']
#         # instance.lname = validated_data['lname']
#         # instance.email = validated_data['email']
#         # instance.username = validated_data['username']
        
#         for field, value in validated_data.items():
#             setattr(instance,field,value)
#         instance.save()
        
#         return instance



# class UpdateProfileSerializer(serializers.Serializer):
#     user = serializers.CharField()
#     userfname = serializers.CharField(source="user.fname")
#     userlname = serializers.CharField(source="user.lname")
#     useremail = 
    
#     class Meta:
#         model = Profile
#         fields = ['user', 'bio', 'bgimage' , 'image', 'followers', 'userfname', 'userlname']


class UserSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    userfname = serializers.CharField(source="user.fname")
    userlname = serializers.CharField(source="user.lname")
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'bgimage' , 'image', 'followers', 'userfname', 'userlname']


class RegisterSerializer(serializers.ModelSerializer):
    fname = serializers.CharField(max_length=255)
    lname = serializers.CharField(max_length=255)
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('fname', 'lname', 'email', 'username', 'password')

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        fname = attrs.get('fname','')
        lname = attrs.get('lname', '')

        if not fname:
            raise serializers.ValidationError("First name is Required")
        
        if not lname:
            raise serializers.ValidationError("Last name is Required")
        

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should only contain alphanumeric chracter")
        return attrs

    def create(self, validated_data):
        # print(validated_data)
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data['email'],
            fname=validated_data['fname'],
            lname=validated_data['lname']
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens', 'pk', 'fname', 'lname']

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
