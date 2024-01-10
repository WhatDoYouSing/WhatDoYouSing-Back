from rest_framework import serializers
from .models import *
from django.db.models import Q
from rest_framework.serializers import ReadOnlyField
from datetime import datetime, timedelta

class FunctionMixin:
    
    def get_author_nickname(self, obj):
        return obj.author.nickname
    
    def get_author_profile(self, obj):
        return obj.author.profile
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comment_count(self, obj):
        return obj.comment.count() 
    
    def get_recomments_count(self, obj):
        return obj.recomments.count()
    
    def get_com_count(self, obj):
        comment_count = obj.comment_count()
        recomment_count = obj.recomment_count()

        return comment_count + recomment_count
    
    def get_com_likes_count(self, obj):
        return obj.com_likes.count()
    
    def get_com_relikes_count(self, obj):
        return obj.com_relikes.count()
    
    def get_is_scraped(self, obj):
        request_user = self.context['request'].user
        return request_user in obj.scrap.all()
    
    
class PostSerializer(FunctionMixin, serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()
    author_profile = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [ 
            "id",
            "author",
            "author_nickname",
            "author_profile",
            "lyrics",
            "content",
            "title",
            "singer",
            "link",
            "sings_emotion",
            "likes_count",
            "scrap",
            #"is_scraped",
            "created_at",
        ]

        read_only_fields = ["author"]

class PostGetSerializer(FunctionMixin, serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()
    author_profile = serializers.SerializerMethodField()
    is_scraped = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [ 
            "id",
            "author",
            "author_nickname",
            "author_profile",
            "lyrics",
            "content",
            "title",
            "singer",
            "link",
            "sings_emotion",
            "likes_count",
            "scrap",
            "is_scraped",
            "created_at",
        ]

        read_only_fields = ["author"]

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Emotion
        fields=['emo_id','content','emo_post','emo_user']

class EmotionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Emotion
        fields = ['emo_user','content']