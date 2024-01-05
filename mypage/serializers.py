from rest_framework import serializers
from .models import User, MyPage

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','nickname','profile']

'''
class ScrapCollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPage

class SingsCollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPage

class CommentsCollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPage

class EmotionsCollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPage
'''