from rest_framework import serializers
from .models import *
from django.db.models import Q
from rest_framework.serializers import ReadOnlyField
from datetime import datetime, timedelta

class FunctionMixin:

    def get_author_nickname(self, obj):
        return obj.author.nickname
    
    def get_comment_count(self, obj):
        return obj.comment.count() 
    
    def get_recomments_count(self, obj):
        return obj.recomments.count()
    
    def get_likes_count(self, obj):
        return obj.com_likes.count()
    
    def get_relikes_count(self, obj):
        return obj.com_relikes.count()
    
class RecommentSerializer(FunctionMixin, serializers.ModelSerializer):
    relikes_count = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Recomment
        fields = [
            "recomment_id",
            "author",
            "author_nickname",
            "com_content",
            "com_relikes",
            "relikes_count",
        ]
    read_only_fields = ["author"]


class CommentSerializer(FunctionMixin, serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    recomments = RecommentSerializer(many=True, read_only=True)
    recomments_count = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "comment_id",
            "author",
            "author_nickname",
            "com_content",
            "com_likes",
            "likes_count",
            "recomments",
            "recomments_count",
        ]
    read_only_fields = ["author"]


