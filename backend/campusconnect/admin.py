from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'
    filter_horizontal = ('skills', 'interests')

class LecturerProfileInline(admin.StackedInline):
    model = LecturerProfile
    can_delete = False
    verbose_name_plural = 'Lecturer Profile'
    filter_horizontal = ('skills', 'interests')

class AdminProfileInline(admin.StackedInline):
    model = AdminProfile
    can_delete = False
    verbose_name_plural = 'Admin Profile'

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')

    inlines = []  # empty default

    def get_inlines(self, request, obj=None):
        """Attach correct profile inline depending on user_type"""
        if obj:
            if obj.user_type == "student":
                return [StudentProfileInline]
            elif obj.user_type == "lecturer":
                return [LecturerProfileInline]
            elif obj.user_type == "admin":
                return [AdminProfileInline]
        return []

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)
    


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('text_content', 'user__username')
    date_hierarchy = 'created_at'

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_at', 'is_public')
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'description')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'message', 'read', 'created_at')
    list_filter = ('notification_type', 'read')
    search_fields = ('message', 'user__username')
    date_hierarchy = 'created_at'

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'start_time', 'end_time', 'is_public')
    list_filter = ('is_public', 'start_time')
    search_fields = ('title', 'description')

class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'file_type', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('title', 'description')

# Register all models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Skill)
admin.site.register(Interest)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Tag)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMembership)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(SharedFile, SharedFileAdmin)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(GroupChat)