from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Registros


class RegistrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registros
        fields = ("title", "description", "created_date", "author")

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.created_date = validated_data.get("created_date", instance.created_date)
        instance.author = validated_data.get("author", instance.author)
        instance.save()
        return instance


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")