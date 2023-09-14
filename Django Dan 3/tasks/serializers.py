from rest_framework import serializers
from django.contrib.auth.models import User


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=64)
    description = serializers.CharField(
        max_length=1024, required=False, allow_blank=True
    )
    is_completed = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    def validate_title(self, value):
        if len(value)<7:
            raise serializers.ValidationError('Title length must be at least 7 characters !')
        return value
    
    def validate(self, data):
        if (data.get('title') and data.get('description') and data['title'] == data['description']):
            raise serializers.ValidationError('Title and description cannot be the same !')
        return data
    
    def create(self, validated):
        return Task.objects.create(**validated_data)
    
    def update(self, task, validated_data):
        instance.title=validated_data['title']
        instance.description = validated_data.get('description',instance.description)
        instance.is_completed = validated_data.get('is_completed',instance._is_completed)
        instance.user = validated_data.get('user',instance.user)