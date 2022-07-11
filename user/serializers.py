from rest_framework import serializers
from .models import (
    User as UserModel,
    UserProfile as UserProfileModel,
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileModel
        fields = "__all__"
