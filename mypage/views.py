from django.shortcuts import render
from rest_framework import views
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from operator import attrgetter

from posts.models import *
from posts.serializers import *
from comments.models import *
from comments.serializers import *
# Create your views here.

class ProfileView(views.APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]  # 필요에 따라 인증 클래스 추가
    permission_classes = [IsAuthenticated] 

    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(request.user) 
        return Response({'message': '마이페이지 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)
    
class ScrapsCollectView(views.APIView):
    def get(self,request):
        user = request.user
        myScraps = Post.objects.filter(scrap=user).order_by('-created_at')
        myScraps_serializers = [PostSerializer(post).data for post in myScraps]

        return Response(myScraps_serializers)
    

class PostsCollectView(views.APIView):
    def get(self,request):
        myPosts = Post.objects.filter(author=request.user).order_by('-created_at')
        myPosts_serializers = [PostSerializer(Post) for Post in myPosts]
        myPosts_data = [myPosts_serializer.data for myPosts_serializer in myPosts_serializers]

        return Response(myPosts_data)
  

class CommentsCollectView(views.APIView):
    def get(self, request):
        myComments = Comment.objects.filter(author=request.user)
        myRecomments = Recomment.objects.filter(author=request.user)

        # Combine Comment and Recomment instances into a single list
        combined_instances = list(myComments) + list(myRecomments)

        # Sort the combined list based on created_at in descending order
        combined_instances.sort(key=attrgetter('created_at'), reverse=True)

        # Serialize the sorted combined instances
        combined_serializers = [
            MypageCommentSerializer(instance) if isinstance(instance, Comment) else RecommentSerializer(instance)
            for instance in combined_instances
        ]

        combined_data = [serializer.data for serializer in combined_serializers]

        Cdata = {
            '내가 쓴 댓글/대댓글 최신순 정렬': combined_data
        }

        return Response(Cdata)
    
'''
class EmotionsCollectView(views.APIView):
'''