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
    skills = serializers.SlugRelatedField(
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
            'id', 'user', 'content_type', 'content',
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

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ['id']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    replies = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at', 'parent_comment', 'replies', 'likes_count']
        read_only_fields = ['user', 'created_at', 'replies', 'likes_count']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

    def get_likes_count(self, obj):
        return obj.like_set.count()
    
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['id']

class GroupMembershipSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    group = serializers.StringRelatedField()
    
    class Meta:
        model = GroupMembership
        fields = '__all__'
        read_only_fields = ['user', 'group', 'joined_at']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']

class GroupPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = GroupPost
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)

    class Meta:
        model = Conversation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'timestamp']

class GroupChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer', 'created_at']

class SharedFileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SharedFile
        fields = '__all__'
        read_only_fields = ['user', 'uploaded_at']
