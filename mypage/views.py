from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from operator import attrgetter
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .pagination import PaginationHandlerMixin

from posts.models import *
from posts.serializers import *
from comments.models import *
from comments.serializers import *

from posts.models import Emotion
# Create your views here.

class ProfileView(views.APIView):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]  # 필요에 따라 인증 클래스 추가
    #permission_classes = [IsAuthenticated] 

    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(request.user) 
        return Response({'message': '마이페이지 조회 성공', 'data': serializer.data}, status=status.HTTP_200_OK)

class MypagePagination(PageNumberPagination):
    page_size = 15

class ScrapsCollectView(views.APIView, PaginationHandlerMixin):
    pagination_class = MypagePagination

    def get(self,request):
        page_number = self.request.query_params.get('page', 1)

        user = request.user
        myScraps = Post.objects.filter(scrap=user).order_by('-created_at')
        myScraps = self.paginate_queryset(myScraps)
        myScraps_serializers = [PostSerializer(post).data for post in myScraps]

        total_scraps = Post.objects.filter(scrap=user).count()
        total_pages = self.paginator.page.paginator.num_pages if self.paginator else 0
        current_page = self.paginator.page.number if self.paginator and self.paginator.page else 1

        response_data = {
            'total': total_scraps,
            'total_page': total_pages,
            'current_page': current_page,
            '내가 스크랩한 게시물': myScraps_serializers,
        }

        return Response(response_data)
    

class PostsCollectView(views.APIView, PaginationHandlerMixin):
    pagination_class = MypagePagination

    def get(self, request):
        page_number = self.request.query_params.get('page', 1)

        myPosts = Post.objects.filter(author=request.user).order_by('-created_at')
        myPosts = self.paginate_queryset(myPosts)
        
        myPosts_serializers = [PostSerializer(post).data for post in myPosts]

        total_posts = Post.objects.filter(author=request.user).count()
        total_pages = self.paginator.page.paginator.num_pages if self.paginator else 0
        current_page = self.paginator.page.number if self.paginator and self.paginator.page else 1

        response_data = {
            'total': total_posts,
            'total_page': total_pages,
            'current_page': current_page,
            '내가 작성한 게시물': myPosts_serializers,
        }

        return Response(response_data)
  

class CommentsCollectView(views.APIView, PaginationHandlerMixin):
    pagination_class = MypagePagination

    def get(self, request):
        page_number = self.request.query_params.get('page', 1)

        myComments = Comment.objects.filter(author=request.user)
        myRecomments = Recomment.objects.filter(author=request.user)

        combined_instances = list(myComments) + list(myRecomments)
        combined_instances.sort(key=attrgetter('created_at'), reverse=True)
        combined_instances = self.paginate_queryset(combined_instances)

        total_comments = Comment.objects.filter(author=request.user).count()
        total_recomments = Recomment.objects.filter(author=request.user).count()
        total_combined = total_comments + total_recomments
        total_pages = self.paginator.page.paginator.num_pages if self.paginator else 0
        current_page = self.paginator.page.number if self.paginator and self.paginator.page else 1
    
        # Serialize the sorted combined instances
        combined_serializers = [
            MypageCommentSerializer(instance) if isinstance(instance, Comment) else RecommentSerializer(instance)
            for instance in combined_instances
        ]

        combined_data = [serializer.data for serializer in combined_serializers]

        Cdata = {
            'total': total_combined,
            'total_page': total_pages,
            'current_page': current_page,
            '내가 쓴 댓글/대댓글 최신순 정렬': combined_data
        }

        return Response(Cdata)


class EmotionsCollectView(views.APIView, PaginationHandlerMixin):
    pagination_class = MypagePagination

    def get(self, request):
        page_number = self.request.query_params.get('page', 1)

        emotion_content = self.request.query_params.get('emotion_content', None)
        myEmotions = Emotion.objects.filter(emo_user=self.request.user)

        myEmotions = myEmotions.filter(Q(content__icontains=emotion_content))
        myEmotions = self.paginate_queryset(myEmotions)

        myEmotionsData = []
        for emotion in myEmotions:
            emotion_data = {
                'emotion': emotion.get_content_display(),  # 감정 내용 가져오기
                'post_data': PostSerializer(emotion.emo_post).data  # 해당 감정이 등록된 포스트 정보 가져오기
            }
            myEmotionsData.append(emotion_data)

        total_emotions = Emotion.objects.filter(emo_user=request.user).count()
        total_pages = self.paginator.page.paginator.num_pages if self.paginator else 0
        current_page = self.paginator.page.number if self.paginator and self.paginator.page else 1

        response_data = {
            'total': total_emotions,
            'total_page': total_pages,
            'current_page': current_page,
            '내가 남긴 감정': myEmotionsData,
        }

        return Response(response_data)
