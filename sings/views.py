import random
import math

from django.shortcuts import render, get_object_or_404
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import *
from posts.models import *
from comments.models import *
from mypage.models import *
from .serializers import *
from .pagination import PaginationHandlerMixin
from comments.serializers import CommentSerializer, RecommentSerializer
from django.db.models import Q, Count
from rest_framework.permissions import IsAuthenticated


# 댓글순(defalut) 홈화면 - 가장 좋아요 많이 받은 가사 5개, 댓글 Top10
class HomeCommentsView(views.APIView):
    def get(self, request):
        # 가장 좋아요 많이 받은 게시물 5개
        most_likes = Post.objects.order_by("-likes_count")[:5]
        most_likes_seri = LikesSerializer(most_likes, many=True)

        # 댓글순으로 Top10 게시물
        top_comments = Post.objects.annotate(
            comments_count=Count("comment") + Count("comments")
        ).order_by("-comments_count")[:10]
        top_comments_seri = TopSerializer(top_comments, many=True)

        data = {
            "Likes": most_likes_seri.data,
            "LankingList": top_comments_seri.data,
        }

        return Response(
            {"message": "홈 댓글순 조회 성공", "data": data}, status=status.HTTP_200_OK
        )


# 최신순 홈화면
class HomeLatestView(views.APIView):
    def get(self, request):
        # 가장 좋아요 많이 받은 게시물 5개
        most_likes = Post.objects.order_by("-likes_count")[:5]
        most_likes_seri = LikesSerializer(most_likes, many=True)

        # 최신순으로 Top 10 게시물
        top_latest = Post.objects.order_by("-created_at")[:10]
        top_latest_seri = TopSerializer(top_latest, many=True)

        data = {
            "Likes": most_likes_seri.data,
            "LankingList": top_latest_seri.data,
        }

        return Response(
            {"message": "홈 최신순 조회 성공", "data": data}, status=status.HTTP_200_OK
        )


# 좋아요순 홈화면
class HomeLikesView(views.APIView):
    def get(self, request):
        # 가장 좋아요 많이 받은 게시물 5개
        most_likes = Post.objects.order_by("-likes_count")[:5]
        most_likes_seri = LikesSerializer(most_likes, many=True)

        # 좋아요순으로 Top 10 게시물
        top_likes = Post.objects.order_by("-likes_count")[:10]
        top_likes_seri = TopSerializer(top_likes, many=True)

        data = {
            "Likes": most_likes_seri.data,
            "LankingList": top_likes_seri.data,
        }

        return Response(
            {"message": "홈 좋아요순 조회 성공", "data": data},
            status=status.HTTP_200_OK,
        )


"""
#추천페이지
class RecommendView(views.APIView):
    def get(self, request):
        all_posts = Post.objects.all()
        ran_size = min(60, len(all_posts))  # 리스트 크기보다 크지 않은 값을 선택
        random_posts = random.sample(list(all_posts), ran_size)
        random_posts_seri = RecommendSerializer(random_posts,many=True)

        return Response({'message': '추천게시물 조회 성공', 'data': random_posts_seri.data}, status=status.HTTP_200_OK)
"""


# 추천시스템 1안으로 수정
class RecommendView(views.APIView):
    def get(self, request):
        # 로그인 했을 때 -> 새로운 추천시스템(1안)
        if request.user.is_authenticated:  # Check if the user is authenticated
            # (1)내가 저장한 (북마크) 게시물의 감정 가져오기
            saved_emotions = Emotion.objects.filter(emo_post__scrap=request.user)
            # (2)내가 감정을 남긴 게시물의 감정 가져오기
            emo_emotions = Emotion.objects.filter(emo_post__content=request.user)
            # (3)내가 댓글을 남긴 게시물의 감정 가져오기
            user_comments = Comment.object.filter(author=request.user)
            commented_posts_pks = user_comments.values_list("post__pk", flat=True)
            commented_emotions = Emotion.objects.filter(
                emo_post_id__in=commented_posts_pks
            )
            # (4)내가 남긴 가사의 감정 가져오기
            lyric_emotions = Emotion.objects.filter(emo_post__author=request.user)

            # 4가지 경로로 가져온 감정 쿼리셋 합산
            all_emotions = (
                saved_emotions | emo_emotions | commented_emotions | lyric_emotions
            )

            # 종합된 감정을 추천에 활용하기 위해 감정 태그를 리스트로 변환
            all_emotion_tags = [emotion.content for emotion in all_emotions]

            # 1~4위 감정 추출
            top_emotions = sorted(
                set(all_emotion_tags), key=all_emotion_tags.count, reverse=True
            )[:4]

            # 5위~12위 감정 추출
            other_emotions = sorted(
                set(all_emotion_tags), key=all_emotion_tags.count, reverse=True
            )[4:12]

            # 상위 감정 태그를 가진 게시물 70%로 추천
            recommended_posts_70_percent = Post.objects.filter(
                sings_emotion__in=top_emotions
            ).order_by("?")[:7]

            # 나머지 감정 태그를 가진 게시물 30%로 추천
            recommended_posts_30_percent = Post.objects.filter(
                sings_emotion__in=other_emotions
            ).order_by("?")[:3]

            recommended_posts = (
                recommended_posts_70_percent | recommended_posts_30_percent
            )

            recommended_posts_seri = RecommendSerializer(recommended_posts, many=True)

            return Response(
                {
                    "message": "로그인 유저 추천게시물 조회 성공",
                    "data": recommended_posts_seri.data,
                },
                status=status.HTTP_200_OK,
            )

        # 로그인 안했을 때 -> 기존의 추천 시스템(랜덤 pk값으로 추천 게시물 선정)
        else:
            all_posts = Post.objects.all()
            ran_size = min(10, len(all_posts))  # 리스트 크기보다 크지 않은 값을 선택
            random_posts = random.sample(list(all_posts), ran_size)
            random_posts_seri = RecommendSerializer(random_posts, many=True)

            return Response(
                {
                    "message": "비로그인 유저 추천게시물 조회 성공",
                    "data": random_posts_seri.data,
                },
                status=status.HTTP_200_OK,
            )


class BoothPagination(PageNumberPagination):
    page_size = 15


# 가사 검색 최신순 정렬
class SearchLatestView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination

    def get(self, request):
        keyword = request.GET.get("keyword")
        emo = request.GET.get("emo")

        posts = Post.objects.all()

        if keyword:
            posts = posts.filter(Q(lyrics__icontains=keyword))

        if emo:
            # posts = posts.filter(Q(sings_emotion__iexact=emo))
            posts = posts.filter(Q(sings_emotion__iexact=str(emo)))

        posts_latest = posts.order_by("-created_at")

        total = posts_latest.__len__()
        total_page = math.ceil(total / 15)
        posts_latest = self.paginate_queryset(posts_latest)

        posts_latest_seri = SearchSerializer(posts_latest, many=True)

        return Response(
            {
                "message": "최신순 가사 검색 성공",
                "total": total,
                "total_page": total_page,
                "current_page": self.current_page,
                "data": posts_latest_seri.data,
            },
            status=status.HTTP_200_OK,
        )


# 가사 검색 좋아요순 정렬
class SearchLikesView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination

    def get(self, request):
        keyword = request.GET.get("keyword")
        emo = request.GET.get("emo")

        posts = Post.objects.all()

        if keyword:
            posts = posts.filter(Q(lyrics__icontains=keyword))

        if emo:
            posts = posts.filter(Q(sings_emotion__iexact=str(emo)))

        posts_likes = posts.order_by("-likes_count")

        total = posts_likes.__len__()
        total_page = math.ceil(total / 15)
        posts_likes = self.paginate_queryset(posts_likes)

        posts_likes_seri = SearchSerializer(posts_likes, many=True)

        return Response(
            {
                "message": "좋아요순 가사 검색 성공",
                "total": total,
                "total_page": total_page,
                "current_page": self.current_page,
                "data": posts_likes_seri.data,
            },
            status=status.HTTP_200_OK,
        )


# 가사 검색 댓글순 정렬
class SearchCommentsView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination

    def get(self, request):
        keyword = request.GET.get("keyword")
        emo = request.GET.get("emo")

        posts = Post.objects.all()

        if keyword:
            posts = posts.filter(Q(lyrics__icontains=keyword))

        if emo:
            posts = posts.filter(Q(sings_emotion__iexact=str(emo)))

        posts_comments = posts.annotate(
            comments_count=Count("comment") + Count("comments")
        ).order_by("-comments_count")

        total = posts_comments.__len__()
        total_page = math.ceil(total / 15)
        posts_comments = self.paginate_queryset(posts_comments)

        posts_comments_seri = SearchSerializer(posts_comments, many=True)

        return Response(
            {
                "message": "댓글순 가사 검색 성공",
                "total": total,
                "total_page": total_page,
                "current_page": self.current_page,
                "data": posts_comments_seri.data,
            },
            status=status.HTTP_200_OK,
        )


"""
#감정태그 최신순 정렬
class SearchEmoLatestView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination
    
    def get(self, request):
        emo = request.GET.get('emo')

        posts = Post.objects.filter(Q(sings_emotion__iexact=str(emo)))
        
        posts_latest = posts.order_by('-created_at')

        total = posts_latest.__len__()
        total_page = math.ceil(total/15)
        posts_latest = self.paginate_queryset(posts_latest)
        posts_latest_seri = SearchSerializer(posts_latest, many=True)
        
        return Response({'message': '감정태그 최신순 검색 성공', 'total': total, 'total_page' : total_page, 'current_page': self.current_page, 'data': {"sings": posts_latest_seri.data}}, status=status.HTTP_200_OK)
        

#감정태그 좋아요순 정렬
class SearchEmoLikesView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination
    
    def get(self, request):
        emo = request.GET.get('emo')
        
        posts = Post.objects.filter(Q(sings_emotion__iexact=str(emo)))
        
        posts_likes = posts.order_by('-likes_count')

        total = posts_likes.__len__()
        total_page = math.ceil(total/15)
        posts_likes = self.paginate_queryset(posts_likes)
        posts_likes_seri = SearchSerializer(posts_likes, many=True)
        
        return Response({'message': '감정태그 좋아요순 검색 성공', 'total': total, 'total_page' : total_page, 'current_page': self.current_page, 'data': {"sings": posts_likes_seri.data}}, status=status.HTTP_200_OK)
        

#감정태그 댓글순 정렬
class SearchEmoCommentsView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination
    
    def get(self, request):
        emo = request.GET.get('emo')
        
        posts = Post.objects.filter(Q(sings_emotion__iexact=str(emo)))
     
        posts_comments = posts.annotate(comments_count=Count('comment')+Count('comments')).order_by('-comments_count')
        
        total = posts_comments.__len__()
        total_page = math.ceil(total/15)
        posts_comments = self.paginate_queryset(posts_comments)
        posts_comments_seri = SearchSerializer(posts_comments, many=True)
        
        return Response({'message': '감정태그 댓글순 검색 성공', 'total': total, 'total_page' : total_page, 'current_page': self.current_page, 'data': {"sings": posts_comments_seri.data}}, status=status.HTTP_200_OK)
"""
