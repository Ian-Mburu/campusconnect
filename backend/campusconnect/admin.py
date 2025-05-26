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

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    filter_horizontal = ('skills', 'interests')

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
admin.site.register(UserProfile)
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