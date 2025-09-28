from rest_framework import serializers #type: ignore
from .models import CustomUser, StudentProfile, LecturerProfile, AdminProfile, Skill, Interest, Post, Group, Notification, Comment, Like, Tag, GroupMembership, Course, GroupPost, Conversation, Message, GroupChat, Event, SharedFile
from django.contrib.auth import get_user_model



CustomUser = get_user_model()


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        depth = 1  # To include related fields like courses, skills, interests

class LecturerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerProfile
        fields = '__all__'
        depth = 1  # To include related fields like skills, interests

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = '__all__'
        depth = 1  # To include related fields if any

class UnifiedProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    user_type = serializers.CharField()
    profile = serializers.SerializerMethodField()


    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'profile']

    def get_profile(self, obj):
       

        if obj.user_type == "student" and hasattr(obj, "student_profile"):
            student = obj.student_profile
            return({
                "department": student.department,
                "year_of_study": student.year_of_study,
                "skills": [s.name for s in student.skills.all()],
                "interests": [i.name for i in student.interests.all()],
            })

        elif obj.user_type == "lecturer" and hasattr(obj, "lecturer_profile"):
            lecturer = obj.lecturer_profile
            return({
                "department": lecturer.department,
                "subjects_taught": lecturer.subjects_taught,
                "research_interests": lecturer.research_interests,
                "skills": [s.name for s in lecturer.skills.all()],
                "interests": [i.name for i in lecturer.interests.all()],
            })

        elif obj.user_type == "admin" and hasattr(obj, "admin_profile"):
            admin = obj.admin_profile
            return({
                "role": getattr(admin, "role", None),
                "office": getattr(admin, "office", None),
            })

        return None



class UserSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(read_only=True)
    lecturer_profile = LecturerProfileSerializer(read_only=True)
    admin_profile = AdminProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'date_joined', 'student_profile', 'lecturer_profile', 'admin_profile']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'date_joined', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            user_type=validated_data.get('user_type', 'student')
        )
        # Auto create correct profile
        if user.user_type == "student":
            StudentProfile.objects.create(user=user)
        elif user.user_type == "lecturer":
            LecturerProfile.objects.create(user=user)
        elif user.user_type == "admin":
            AdminProfile.objects.create(user=user)
        return user

    # def to_internal_value(self, data):
    #     # let DRF parse normally first
    #     ret = super().to_internal_value(data)

    #     # handle case where frontend sends comma-separated strings
    #     if "skills" in data and isinstance(data["skills"], str):
    #         ret["skills"] = [s.strip() for s in data["skills"].split(",") if s.strip()]

    #     if "interests" in data and isinstance(data["interests"], str):
    #         ret["interests"] = [i.strip() for i in data["interests"].split(",") if i.strip()]

    #     return ret

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
        read_only_fields = ['id', 'name']

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
        fields = ['id', 'name']

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
