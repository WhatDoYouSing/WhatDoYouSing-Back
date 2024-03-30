from rest_framework import serializers
from .models import User, Post
from comments.models import Recomment

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','nickname','profile']

class EmotionsFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'sings_emotion', 'lyrics', 'title', 'singer']

class RecommentGetSerializer(serializers.ModelSerializer):
    relikes_count = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()
    author_profile = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    class Meta:
        model = Recomment
        fields = [
            "recomment_id",
            "post",
            "author",
            "author_nickname",
            "author_profile",
            "com_content",
            "relikes_count",
            "liked_by_user",
            "created_at"
        ]
    read_only_fields = ["author"]

    def get_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.com_relikes.all()
        return False
    def get_author_nickname(self, obj):
        return obj.author.nickname
    def get_author_profile(self, obj):
        return obj.author.profile
    def get_relikes_count(self, obj):
        return obj.com_relikes.count()
    def get_post(self, obj):
        return obj.comment.post.id