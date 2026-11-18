from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get("email"),
            password=validated_data.get("password")
        )
        return user