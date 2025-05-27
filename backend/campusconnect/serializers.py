from rest_framework import serializers #type: ignore
from . models import *


class UserSerializer(serializers.ModelSerializer):
    profile_url = serializers.HyperlinkedIdentityField(
        view_name='userprofile-detail',
        lookup_field='username',
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'profile_url', 'date_joined']

        extra_kwargs = {'password': {'write_only': True}}    


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    Skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all(),
    )

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'user', 'content_type', 'text_content',
            'image', 'video', 'created_at', 'likes_count',
            'comments_count'
        ]
        read_only_fields = ['user']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['creator']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user', 'created_at']