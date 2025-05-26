from rest_framework import serializers #type: ignore
from . models import *


class UserSerializer(serializers.modelSerializer):
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
    Skills = serializers.slugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all(),
    )

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']