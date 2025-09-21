from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('lecturer', 'lecturer'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    bio = models.TextField(blank=True, null=True, max_length=500)
    profile_picture = models.ImageField(upload_to='image', default='default/default-user.jpg', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Interest(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    year_of_study = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    courses = models.ManyToManyField('Course', blank=True, related_name="students")
    skills = models.ManyToManyField('Skill', blank=True)
    interests = models.ManyToManyField('Interest', blank=True)

    def __str__(self):
        return f"StudentProfile: {self.user.username}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_profile")
    department = models.CharField(max_length=100, blank=True, null=True)
    subjects_taught = models.TextField(blank=True, null=True)
    research_interests = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField('Skill', blank=True)
    interests = models.ManyToManyField('Interest', blank=True)

    def __str__(self):
        return f"TeacherProfile: {self.user.username}"


class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="admin_profile")
    role_description = models.TextField(blank=True, null=True)
    office_location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"AdminProfile: {self.user.username}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    enrolled_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


 # Social Media/Posts   

class Post(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('link', 'Link'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"
    
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post', 'comment')

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

# Communities/Groups

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(CustomUser, through='GroupMembership')
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='groups/avatars/', blank=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class GroupMembership(models.Model):
    ROLES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator')
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'group')
    
    def __str__(self):
        return f"{self.user.username} in {self.group.name}"

class GroupPost(Post):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_posts')


# Messaging system
class Conversation(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"

class GroupChat(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='group_chat')
    messages = models.ManyToManyField(Message, blank=True)


# Notification system

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('message', 'Message'),
        ('group_invite', 'Group Invite'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=15, choices=NOTIFICATION_TYPES)
    message = models.CharField(max_length=255)
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    related_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    link = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
    

# Event calendar system

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organized_events')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    attendees = models.ManyToManyField(CustomUser, related_name='events_attending', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    

# File sharing

class SharedFile(models.Model):
    FILE_TYPES = (
        ('document', 'Document'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='shared_files/')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    allowed_users = models.ManyToManyField(CustomUser, related_name='accessible_files', blank=True)
    groups = models.ManyToManyField(Group, related_name='group_files', blank=True)
    
    def __str__(self):
        return self.title