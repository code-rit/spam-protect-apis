from rest_framework import serializers
from .models import User, Contact, SpamMark

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone_number', 'email', 'is_favorite', 'owner']


class SpamMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamMark
        fields = ['id', 'contact', 'marked_by', 'created_at']
