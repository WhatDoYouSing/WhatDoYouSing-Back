from rest_framework import serializers
from .models import *
from django.db.models import Q
from rest_framework.serializers import ReadOnlyField
from datetime import datetime, timedelta

class FunctionMixin:
    
    def get_author_nickname(self, obj):
        return obj.author.nickname
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comment_count(self, obj):
        return obj.comment.count() 
    
    def get_recomments_count(self, obj):
        return obj.recomments.count()
    
    def get_com_likes_count(self, obj):
        return obj.com_likes.count()
    
    def get_com_relikes_count(self, obj):
        return obj.com_relikes.count()
    
    
class PostSerializer(FunctionMixin, serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField() 
    author_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [ 
            "id",
            "author",
            "author_nickname",
            "lyrics",
            "content",
            "title",
            "singer",
            "link",
            "sings_emotion",
            "likes_count",
            "scrap",
            "comment_count",
        ]

        read_only_fields = ["author"]
