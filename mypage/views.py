from django.shortcuts import render
from rest_framework import views
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

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
        myScraps = Post.objects.filter(scrap__in=[user])
        myScraps_serializers = [PostSerializer(post).data for post in myScraps]

        return Response(myScraps_serializers)
    

class PostsCollectView(views.APIView):
    def get(self,request):
        myPosts = Post.objects.filter(author=request.user)
        myPosts_serializers = [PostSerializer(Post) for Post in myPosts]
        myPosts_data = [myPosts_serializer.data for myPosts_serializer in myPosts_serializers]

        return Response(myPosts_data)
  

class CommentsCollectView(views.APIView):
    def get(self,request):
        myComments = Comment.objects.filter(author=request.user)
        myRecomments = Recomment.objects.filter(author=request.user)

        myComments_serializers = [CommentSerializer(Comment) for Comment in myComments]
        myRecomments_serializers = [RecommentSerializer(Recomment) for Recomment in myRecomments]

        myComments_data = [myComments_serializer.data for myComments_serializer in myComments_serializers]
        myRecomments_data = [myRecomments_serializer.data for myRecomments_serializer in myRecomments_serializers]

        Cdata = {
            'myComments': myComments_data,
            'myRecomments':myRecomments_data
        }

        return Response(Cdata)

'''
class EmotionsCollectView(views.APIView):
'''