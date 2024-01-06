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

class CommentView(views.APIView):
    serializer_class = CommentSerializer

    def get(self, request, post_pk, format=None):
        comments = Comment.objects.filter(post_id=post_pk)
        serializer = self.serializer_class(comments, many=True)
        return Response({'message': '댓글조회 성공', 'data': serializer.data})
  
    def post(self, request, post_pk, format=None):
        serializer = CommentSerializer(data={**request.data, 'post': post_pk})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({'message': '댓글작성 성공', 'data': serializer.data})
        else:
            return Response({'message': '댓글 작성 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CommentDelView(views.APIView):

    def delete(self, request,comment_pk, format=None):
        comment = get_object_or_404(Comment, comment_id=comment_pk)
        comment.delete()
        return Response({"message": "댓글 삭제 성공"}, status=status.HTTP_204_NO_CONTENT)


class RecommentView(views.APIView):
    serializer_class = RecommentSerializer

    def post(self, request, comment_pk, format=None):
        comment = get_object_or_404(Comment, pk=comment_pk)
        serializer = RecommentSerializer(data=request.data)
        if serializer.is_valid():
            recomment = serializer.save(comment=comment, author=request.user)
            return Response(
                {"message": "대댓글 작성 성공", "data": serializer.data})
        return Response({"message": "대댓글 작성 실패", "data": serializer.errors})

class RecommentDelView(views.APIView):
    def delete(self, request, recomment_pk, format=None):
        recomment = get_object_or_404(Recomment, recomment_id=recomment_pk)
        recomment.delete()
        return Response({"message": "대댓글 삭제 성공"})
   

class CommentLikeView(views.APIView):

    def get(self, request, comment_pk):
        comment = get_object_or_404(Comment, comment_id=comment_pk)
        liked_by_user = request.user in comment.com_likes.all()
        return Response({"liked": liked_by_user})

    def post(self, request, comment_pk):
        comment = get_object_or_404(Comment, comment_id=comment_pk)
        user = request.user

        if user in comment.com_likes.all():
            comment.com_likes.remove(user)
            liked = False
        else:
            comment.com_likes.add(user)
            liked = True

        return Response({"message": "좋아요 변경 성공", "liked": liked})

class RecommentLikeView(views.APIView):

    def get(self, request, comment_pk, recomment_pk):
        recomment = get_object_or_404(Recomment, comment_id=comment_pk, pk=recomment_pk)
        reliked_by_user = request.user in recomment.com_relikes.all()
        return Response({"reliked": reliked_by_user})

    def post(self, request, comment_pk, recomment_pk):
        recomment = get_object_or_404(Recomment, comment_id=comment_pk, pk=recomment_pk)
        user = request.user

        if user in recomment.com_relikes.all():
            recomment.com_relikes.remove(user)
            reliked = False
        else:
            recomment.com_relikes.add(user)
            reliked = True

        return Response({"message": "대댓글 좋아요 변경 성공", "reliked": reliked})