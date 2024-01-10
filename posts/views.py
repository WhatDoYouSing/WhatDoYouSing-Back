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
    serializer_class = PostGetSerializer

    def get(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"message": "가사가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(post, context={'request': request})
        return Response({"message": "가사 조회 성공", "data": serializer.data}, status=status.HTTP_200_OK)

class PostAddView(views.APIView):
    serializer_class = PostSerializer

    def post(self, request, format=None):  # 게시글 작성 POST 메소드
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"message": "가사 작성 성공", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "가사 작성 실패", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PostDelView(views.APIView):
    serializer_class = PostSerializer

    def delete(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response({"message": "가사 삭제 성공"}, status=status.HTTP_204_NO_CONTENT)
        
class PostScrapView(views.APIView):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        scraped_by_user = request.user in post.scraps.all()

        if not scraped_by_user:  # 혹은 다른 조건에 따라 처리
            return Response({"message": "해당 데이터를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"scraped": scraped_by_user}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user in post.scrap.all():
            post.scrap.remove(user)
            scraped = False
        else:
            post.scrap.add(user)
            scraped = True

        return Response({"message": "스크랩 변경 성공", "scraped": scraped}, status=status.HTTP_200_OK)

class PostLikeView(views.APIView):
    serializer_class = PostSerializer

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.likes_count < 0:
            return Response({"message": "likes_count가 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"likes_count": post.likes_count}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        post.increase_likes_count()  # 좋아요 갯수 증가
        return Response({"message": "좋아요가 추가되었습니다.", "likes_count": post.likes_count}, status=status.HTTP_200_OK)
    
        # post.like_post(user)  # 사용자의 좋아요를 추가합니다.
        # likes_count = post.likes_count()  # 새로운 좋아요 수를 가져옵니다.

        # return Response({"message": "좋아요가 추가되었습니다.", "likes_count": likes_count})


class EmotionDelView(views.APIView):
   
    def delete(self, request, pk):
        now_user = request.user
        #content = request.data.get('content')

        try:
            emotion_to_delete = Emotion.objects.get(emo_post=pk, emo_user=now_user)
            emotion_to_delete.delete()  # 해당 Emotion 삭제
            return Response({"message": "투표감정 삭제 성공"}, status=status.HTTP_200_OK)
        except Emotion.DoesNotExist:
            return Response({"message": "해당하는 감정을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # emo=Emotion.objects.filter(emo_post=post_pk,emo_user=now_user.id,content=content)
        # emo.delete()
        # return Response({"message": "투표감정 삭제 성공"})

##임의로 넣었으니 무시하셔도 됩니다...      
class EmotionFunctionsView(views.APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        
        emotions = Emotion.objects.filter(emo_post=post).values('content').annotate(num=Count('content'))
        now_user = request.user
        my_emotions = Emotion.objects.filter(emo_post=post, emo_user=now_user).values('content')

        data = {
            'post_id': pk,
            'my_emotions': [emotion['content'] for emotion in my_emotions],
            'Emotion': [
                {'content': emotion['content'], 'num': emotion['num']} for emotion in emotions
            ]
        }

        if not emotions:
            return Response({'message': "투표감정 조회 실패"}, status=status.HTTP_200_OK)

        return Response({'message': "투표감정 조회 성공", "data": data}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        content=request.data['content']
        now_user=request.user

        # 해당 사용자와 포스트에 대한 감정 객체 확인
        existing_emotion = Emotion.objects.filter(emo_post=pk, emo_user=now_user)
        
        if existing_emotion.exists():
            emotion = existing_emotion.first()
            serializer = EmotionSerializer(emotion, data={'content': content}, partial=True)
        else:
            serializer = EmotionSerializer(data={
                'content': content,
                'emo_post': post.id,
                'emo_user': now_user.id
            })

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "투표감정 등록 성공", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "투표감정 등록 실패", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





   