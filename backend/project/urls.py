from django.contrib import admin
from django.urls import path

from django.urls import include, path
from rest_framework.routers import DefaultRouter # type: ignore
from campusconnect.views import *
from rest_framework_nested import routers # type: ignore
from rest_framework.authtoken.views import obtain_auth_token # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView #type:ignore



# Base router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'userprofiles', UserProfileViewSet, basename='userprofile')
router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'skills', SkillViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'groupmemberships', GroupMembershipViewSet)
router.register(r'interests', InterestViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'groupposts', GroupPostViewSet)
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'groupchats', GroupChatViewSet)
router.register(r'events', EventViewSet)
router.register(r'sharedfiles', SharedFileViewSet)


# Nested routes
posts_router = routers.NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')
posts_router.register(r'likes', LikeViewSet, basename='post-likes')

groups_router = routers.NestedDefaultRouter(router, r'groups', lookup='group')
groups_router.register(r'members', GroupMembershipViewSet, basename='group-members')
groups_router.register(r'groupposts', GroupPostViewSet, basename='group-posts')

conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/', include(posts_router.urls)),
    path('api/', include(groups_router.urls)),
    path('api/', include(conversations_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
