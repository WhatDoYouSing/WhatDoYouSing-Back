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

    def get(self, request, pk, format=None):
        posts = Post.objects.all()
        if not posts:
            return Response({"message": "포스트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(posts, many=True)
        return Response({"message": "포스트 조회 성공", "data": serializer.data}, status=status.HTTP_200_OK)


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

class EmotionView(views.APIView):

    def post(self, request, post_pk):
        post = get_object_or_404(Post, id=post_pk)
        content=request.data['content']
        now_user=request.user

        # 해당 사용자와 포스트에 대한 감정 객체 확인
        existing_emotion = Emotion.objects.filter(emo_post=post_pk, emo_user=now_user)
        
        # 이미 존재하는 경우 오류 응답
        if existing_emotion.exists():
            return Response({"message": "이미 투표한 감정이 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        emotion=EmotionSerializer(data={
            'content':content,
            'emo_post':post.id,
            'emo_user':now_user.id
        }) 
        if emotion.is_valid():
            emotion.save()
            return Response({"message": "투표감정 등록 성공","data":emotion.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "투표감정 등록 실패","error":emotion.errors},status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, post_pk):
        post = get_object_or_404(Post, id=post_pk)
        emotions=Emotion.objects.filter(emo_post=post).all()
        is_my_1, is_my_2, is_my_3, is_my_4, is_my_5, is_my_6, is_my_7, is_my_8, is_my_9, is_my_10, is_my_11, is_my_12 = [False] * 12

        emotion1s=emotions.filter(content=1).all()
        emotion1count=emotion1s.count()
        for emotion in emotion1s:
            if emotion.emo_user==request.user : is_my_1=True

        emotion2s=emotions.filter(content=2).all()
        emotion2count=emotion2s.count()
        for emotion in emotion2s:
            if emotion.emo_user==request.user : is_my_2=True

        emotion3s=emotions.filter(content=3).all()
        emotion3count=emotion3s.count()
        for emotion in emotion3s:
            if emotion.emo_user==request.user : is_my_3=True

        emotion4s=emotions.filter(content=4).all()
        emotion4count=emotion4s.count()
        for emotion in emotion4s:
            if emotion.emo_user==request.user : is_my_4=True

        emotion5s=emotions.filter(content=5).all()
        emotion5count=emotion5s.count()
        for emotion in emotion5s:
            if emotion.emo_user==request.user : is_my_5=True

        emotion6s=emotions.filter(content=6).all()
        emotion6count=emotion6s.count()
        for emotion in emotion6s:
            if emotion.emo_user==request.user : is_my_6=True

        emotion7s = emotions.filter(content=7).all()
        emotion7count = emotion7s.count()
        for emotion in emotion7s:
            if emotion.emo_user == request.user : is_my_7 = True

        emotion8s = emotions.filter(content=8).all()
        emotion8count = emotion8s.count()
        for emotion in emotion8s:
            if emotion.emo_user == request.user : is_my_8 = True

        emotion9s = emotions.filter(content=9).all()
        emotion9count = emotion9s.count()
        for emotion in emotion9s:
            if emotion.emo_user == request.user : is_my_9 = True

        emotion10s = emotions.filter(content=10).all()
        emotion10count = emotion10s.count()
        for emotion in emotion10s:
            if emotion.emo_user == request.user : is_my_10 = True

        emotion11s = emotions.filter(content=11).all()
        emotion11count = emotion11s.count()
        for emotion in emotion11s:
            if emotion.emo_user == request.user : is_my_11 = True

        emotion12s = emotions.filter(content=12).all()
        emotion12count = emotion12s.count()
        for emotion in emotion12s:
            if emotion.emo_user == request.user : is_my_12 = True
        
        data = {
                'post_id': post_pk,
                'content': post.lyrics,
                'Emotion': [
                    {'content': 1, 'num': emotion1count, 'is_my': is_my_1},
                    {'content': 2, 'num': emotion2count, 'is_my': is_my_2},
                    {'content': 3, 'num': emotion3count, 'is_my': is_my_3},
                    {'content': 4, 'num': emotion4count, 'is_my': is_my_4},
                    {'content': 5, 'num': emotion5count, 'is_my': is_my_5},
                    {'content': 6, 'num': emotion6count, 'is_my': is_my_6},
                    {'content': 7, 'num': emotion7count, 'is_my': is_my_7},
                    {'content': 8, 'num': emotion8count, 'is_my': is_my_8},
                    {'content': 9, 'num': emotion9count, 'is_my': is_my_9},
                    {'content': 10, 'num': emotion10count, 'is_my': is_my_10},
                    {'content': 11, 'num': emotion11count, 'is_my': is_my_11},
                    {'content': 12, 'num': emotion12count, 'is_my': is_my_12},
                ],
            }

        if not any([is_my_1, is_my_2, is_my_3, is_my_4, is_my_5, is_my_6,
            is_my_7, is_my_8, is_my_9, is_my_10, is_my_11, is_my_12]):
            return Response({'message': "투표감정 조회 실패"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': "투표감정 조회 성공", "data": data}, status=status.HTTP_200_OK)
    
    def delete(self, request, post_pk):
        now_user = request.user
        #content = request.data.get('content')

        try:
            emotion_to_delete = Emotion.objects.get(emo_post=post_pk, emo_user=now_user)
            emotion_to_delete.delete()  # 해당 Emotion 삭제
            return Response({"message": "투표감정 삭제 성공"}, status=status.HTTP_200_OK)
        except Emotion.DoesNotExist:
            return Response({"message": "해당하는 감정을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # emo=Emotion.objects.filter(emo_post=post_pk,emo_user=now_user.id,content=content)
        # emo.delete()
        # return Response({"message": "투표감정 삭제 성공"})
      
