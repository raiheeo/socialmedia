from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserProfileListLSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'bio', 'image',
                  'website', 'age', 'phone_number']


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']


class UserProfilePostSerializer(serializers.ModelSerializer):
    follower = UserProfileListSerializer()
    following = UserProfileListSerializer()

    class Meta:
        model = UserProfile
        fields = ['follower', 'following']


class FollowListSerializer(serializers.ModelSerializer):
    follower = UserProfileListSerializer()
    following = UserProfileListSerializer()

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following']


class PostListSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()
    get_count_like = serializers.ModelSerializer()


    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'video', 'hashtag', 'get_count_like']

    def get_count_like(self, obj):
        return obj.get_count_like()


class PostForLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['image', 'video']


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    user_like = UserProfileListSerializer(many=True, read_only=True)
    post_like = PostForLikeSerializer(many=True, read_only=True)
    follow = UserProfilePostSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['user', 'image', 'video', 'hashtag', 'created_at',
                  'user_like', 'post_like', 'follow']


class PostLikeSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()
    post = PostForLikeSerializer()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post', 'like', 'created_at']


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post']


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_at']


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


class StoryListSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Story
        fields = ['id', 'user', 'image', 'video', 'created_at']


class StoryDetailSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Story
        fields = ['user', 'image', 'video', 'created_at']


class SavedSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()

    class Meta:
        model = Saved
        fields = ['id', 'user']


class SavedItemSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    saved = SavedSerializer()
    post = PostForLikeSerializer()

    class Meta:
        model = SavedItem
        fields = ['id', 'post', 'saved', 'created_date']