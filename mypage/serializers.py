from rest_framework import serializers
from .models import User, Post

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','nickname','profile']

class EmotionsFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'sings_emotion', 'lyrics', 'title', 'singer']