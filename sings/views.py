from django.shortcuts import render, get_object_or_404
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from posts.models import *
from comments.models import *
from .serializers import *
from comments.serializers import CommentSerializer, RecommentSerializer
from django.db.models import Q, Count
import random


#댓글순(defalut) 홈화면 - 가장 좋아요 많이 받은 가사 5개, 댓글 Top10
class HomeCommentsView(views.APIView):
    def get(self, request):
        #가장 좋아요 많이 받은 게시물 5개
        most_likes = Post.objects.order_by('-likes_count')[:5]
        most_likes_seri = LikesSerializer(most_likes, many=True)

        #댓글순으로 Top10 게시물
        top_comments = Post.objects.annotate(comments_count=models.F('comment__com_count')).order_by('-comments_count')[:10]
        top_comments_seri = TopSerializer(top_comments, many=True)

        data = {
            'Likes': most_likes_seri.data,
            'LankingComments': top_comments_seri.data,
        }

        return Response({'message': '홈 댓글순 조회 성공', 'data': data}, status=status.HTTP_200_OK) 


#최신순 홈화면
class HomeLatestView(views.APIView):    
    def get(self, request):
        #가장 좋아요 많이 받은 게시물 5개
        most_likes = Post.objects.order_by('-likes_count')[:5]
        most_likes_seri = LikesSerializer(most_likes, many=True)

        #최신순으로 Top 10 게시물
        top_latest = Post.objects.order_by('-created_at')[:10]
        top_latest_seri = TopSerializer(top_latest, many=True)

        data = {
            'Likes': most_likes_seri.data,
            'LankingLatest': top_latest_seri.data,
        }

        return Response({'message': '홈 최신순 조회 성공', 'data': data}, status=status.HTTP_200_OK)


#좋아요순 홈화면
class HomeLikesView(views.APIView):
    def get(self, request):
        #가장 좋아요 많이 받은 게시물 5개
        most_likes = Post.objects.order_by('-likes_count')[:5]
        most_likes_seri = LikesSerializer(most_likes, many=True)

        #좋아요순으로 Top 10 게시물
        top_likes = Post.objects.order_by('-likes_count')[:10]
        top_likes_seri = TopSerializer(top_likes, many=True)

        data = {
            'Likes': most_likes_seri.data,
            'LankingLikes': top_likes_seri.data,
        }

        return Response({'message': '홈 좋아요순 조회 성공', 'data': data}, status=status.HTTP_200_OK)


#추천페이지
class RecommendView(views.APIView):
    def get(self, request):
        all_posts = Post.objects.all()
        ran_size = min(1, len(all_posts))  # 리스트 크기보다 크지 않은 값을 선택
        random_posts = random.sample(list(all_posts), ran_size)
        random_posts_seri = RecommendSerializer(random_posts,many=True)

        return Response({'message': '추천게시물 조회 성공', 'data': random_posts_seri.data}, status=status.HTTP_200_OK)


#가사 검색 최신순 정렬
class SearchLatestView(views.APIView):
    def get(self, request):
        keyword= request.GET.get('keyword')
        emo = request.GET.get('emo')

        posts = Post.objects.filter(Q(lyrics__icontains=keyword))
        
        if emo:
            posts = posts.filter(Q(sings_emotion__iexact=emo))

        posts_latest = posts.order_by('-created_at')
        posts_latest_seri = SearchSerializer(posts_latest, many=True)

        return Response({'message':'최신순 가사 검색 성공', 'data': {"sings": posts_latest_seri.data}}, status=status.HTTP_200_OK)


#가사 검색 좋아요순 정렬
class SearchLikesView(views.APIView):
    def get(self, request):
        keyword= request.GET.get('keyword')
        emo = request.GET.get('emo')

        posts = Post.objects.filter(Q(lyrics__icontains=keyword))
        
        if emo:
            posts = posts.filter(Q(sings_emotion__iexact=emo))

        posts_likes = posts.order_by('-likes_count')
        posts_likes_seri = SearchSerializer(posts_likes, many=True)

        return Response({'message':'좋아요순 가사 검색 성공', 'data': {"sings": posts_likes_seri.data}}, status=status.HTTP_200_OK)


#가사 검색 댓글순 정렬
class SearchCommentsView(views.APIView):
    def get(self, request):
        keyword= request.GET.get('keyword')
        emo = request.GET.get('emo')

        posts = Post.objects.filter(Q(lyrics__icontains=keyword))
        
        if emo:
            posts = posts.filter(Q(sings_emotion__iexact=emo))

        posts_comments = posts.annotate(comments_count=models.F('comment__com_count')).order_by('-comments_count')
        posts_comments_seri = SearchSerializer(posts_comments, many=True)

        return Response({'message':'댓글순 가사 검색 성공', 'data': {"sings": posts_comments_seri.data}}, status=status.HTTP_200_OK)


      
#감정태그 최신순 정렬
class SearchEmoLatestView(views.APIView):
    def get(self, request):
        emo = request.GET.get('emo')

        posts = Post.objects.filter(Q(sings_emotion__iexact=emo))
        
        posts_latest = posts.order_by('-created_at')
        posts_latest_seri = SearchSerializer(posts_latest, many=True)
        
        return Response({'message': '감정태그 최신순 검색 성공', 'data': {"sings": posts_latest_seri.data}}, status=status.HTTP_200_OK)
        

#감정태그 좋아요순 정렬
class SearchEmoLikesView(views.APIView):
    def get(self, request):
        emo = request.GET.get('emo')
        
        posts = Post.objects.filter(Q(sings_emotion__iexact=emo))
        
        posts_likes = posts.order_by('-likes_count')
        posts_likes_seri = SearchSerializer(posts_likes, many=True)
        
        return Response({'message':'감정태그 좋아요순 검색 성공', 'data': {"sings": posts_likes_seri.data}}, status=status.HTTP_200_OK)


#감정태그 댓글순 정렬
class SearchEmoCommentsView(views.APIView):
    def get(self, request):
        emo = request.GET.get('emo')
        
        posts = Post.objects.filter(Q(sings_emotion__iexact=emo))
     
        posts_comments = posts.annotate(comments_count=models.F('comment__com_count')).order_by('-comments_count')
        posts_comments_seri = SearchSerializer(posts_comments, many=True)

        return Response({'message': '감정태그 댓글순 검색 성공', 'data': {"sings": posts_comments_seri.data}}, status=status.HTTP_200_OK)

