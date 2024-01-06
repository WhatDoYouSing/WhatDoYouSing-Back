from rest_framework import serializers
from .models import *
from posts.models import Post
from comments.models import Comment, Recomment
from comments.serializers import RecommentSerializer, CommentSerializer

#가장 좋아요 많이 받은 게시물 5개(메인홈 상단)
class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'sings_emotion', 'likes_count', 'lyrics', 'content', 'title', 'singer']

#홈페이지 Top10
#comment 카운트하는 거 넣어야함!!!
class TopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'lyrics', 'title', 'singer']

#추천게시물
class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'lyrics', 'content', 'title', 'singer']


#검색-> 감정, 가사, 제목, 가수, 좋아요수, 댓글수
class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'sings_emotion', 'lyrics', 'title', 'singer']



'''
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sings
        fields = ['comment', 'recomment']

#홈페이지
class HomeSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    recomment_count = serializers.SerializerMethodField() 

    class Meta:
        model = Sings
        fields = ['id', 'sings_emotion', 'likes_count', 'lyrics', 'content', 'title', 'singer']

    def get_comment_count(self, obj):
        return obj.like.count;
'''    
'''
    def get_comment_count(self, obj):
        return obj.get_comment_count()
    
    def get_like_count(self, obj):
        return obj.get_like_count()
'''


    
'''
#
class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'post', 'comment', 'comment_count', 'like_count']

class SingsSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Sings
        fields = ['id', 'post', 'comment', 'comment_count', 'like_count']

    def get_comment_count(self, obj):
        return obj.get_comment_count()
    
    def get_like_count(self, obj):
        return obj.get_like_count()
'''