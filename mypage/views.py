from django.shortcuts import render
from rest_framework import views
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class ProfileView(views.APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]  # 필요에 따라 인증 클래스 추가
    permission_classes = [IsAuthenticated] 

    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(request.user) 
        return Response({'message': '마이페이지 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)
    
class ScrapCollectView(views.APIView):
    serializer_class = ScrapCollectSerializer

class SingsCollectView(views.APIView):
    serializer_class = SingsCollectSerializer

class CommentsCollectView(views.APIView):
    serializer_class = CommentsCollectSerializer

class EmotionsCollectView(views.APIView):
    serializer_class = EmotionsCollectSerializer