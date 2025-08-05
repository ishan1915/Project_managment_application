from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Group, Task, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = '__all__'

class MyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=['id','name']

class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['group','assigned_to','title','description','deadline']

class TaskSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=['uploaded_file','user_description']

class TaskMarkComplete(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=['is_completed']

class TaskDetailSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    assigned_to = UserSerializer()
    class Meta:
        model = Task
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
