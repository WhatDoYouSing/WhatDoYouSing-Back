from rest_framework import serializers
from .models import *
from django.db.models import Q
from rest_framework.serializers import ReadOnlyField
from datetime import datetime, timedelta

class FunctionMixin:

    def get_author_nickname(self, obj):
        return obj.author.nickname
    
    def get_author_profile(self,obj):
        return obj.author.profile
    
    def get_comment_count(self, obj):
        return obj.comment.count() 
    
    def get_recomments_count(self, obj):
        return obj.recomments.count()
    
    def get_likes_count(self, obj):
        return obj.com_likes.count()
    
    def get_relikes_count(self, obj):
        return obj.com_relikes.count()
    
    def get_com_count(self, obj):
        # 댓글 수 계산
        comment_count = Comment.objects.filter(post=obj.post).count()
        
        # 대댓글 수 계산
        recomment_count = Recomment.objects.filter(comment__post=obj.post).count()
        
        # 댓글과 대댓글 수를 더하여 반환
        return comment_count + recomment_count
     
    '''
    def get_is_liked(self, obj):
        request_user = self.context['request'].user
        return request_user in obj.com_likes.all()
    
    def get_is_reliked(self, obj):
        request_user = self.context['request'].user
        return request_user in obj.com_relikes.all() 
    '''
    
class RecommentSerializer(FunctionMixin, serializers.ModelSerializer):
    relikes_count = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()
    author_profile = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    #is_reliked = serializers.SerializerMethodField()

    class Meta:
        model = Recomment
        fields = [
            "recomment_id",
            "post",
            "author",
            "author_nickname",
            "author_profile",
            "com_content",
            "com_relikes",
            "relikes_count",
            #"is_reliked",
            "created_at"
        ]
    read_only_fields = ["author"]


class CommentSerializer(FunctionMixin, serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    recomments = RecommentSerializer(many=True, read_only=True)
    recomments_count = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()
    author_profile = serializers.SerializerMethodField()
    com_count = serializers.SerializerMethodField()
    #is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "comment_id",
            "post",
            "author",
            "author_nickname",
            "author_profile",
            "com_content",
            "com_likes",
            "likes_count",
            #"is_liked",
            "recomments",
            "recomments_count",
            "com_count",
            "created_at"
        ]
    read_only_fields = ["author"]


class MypageCommentSerializer(FunctionMixin, serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()
    author_profile = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "comment_id",
            "post",
            "author",
            "author_nickname",
            "author_profile",
            "com_content",
            "com_likes",
            "likes_count",
            "created_at"
        ]
    read_only_fields = ["author"]

