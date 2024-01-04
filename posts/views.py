from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import *
from rest_framework import status, permissions
from .permissions import *
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from django.db.models import Q, Count

from .serializers import *
from .models import *

# Create your views here.
class PostListView(views.APIView):
    serializer_class = PostSerializer

    def get(self, request):
        posts = Post.objects.all()  
        serializer = self.serializer_class(posts, many=True)  
        return Response(serializer.data)

class PostView(views.APIView):
    #permission_classes = [IsAuthorOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def post(self, request, format=None):  # 게시글 작성 POST 메소드
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(
                {"message": "포스트 작성 성공", "data": serializer.data}, status=HTTP_200_OK
            )
        return Response({"message": "포스트 작성 실패", "errors": serializer.errors})

    def delete(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response({"message": "게시물 삭제 성공"})
        
class PostScrapView(views.APIView):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        scraped_by_user = request.user in post.scraps.all()
        return Response({"scraped": scraped_by_user})

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        user = request.user

        if user in post.scrap.all():
            post.scrap.remove(user)
            scraped = False
        else:
            post.scrap.add(user)
            scraped = True

        return Response({"message": "스크랩 변경 성공", "scraped": scraped})

class PostLikeView(views.APIView):
    serializer_class = PostSerializer

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return Response({"likes_count": post.likes_count})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        post.increase_likes_count()  # 좋아요 갯수 증가
        return Response({"message": "좋아요가 추가되었습니다.", "likes_count": post.likes_count})
    
        # post.like_post(user)  # 사용자의 좋아요를 추가합니다.
        # likes_count = post.likes_count()  # 새로운 좋아요 수를 가져옵니다.

        # return Response({"message": "좋아요가 추가되었습니다.", "likes_count": likes_count})
