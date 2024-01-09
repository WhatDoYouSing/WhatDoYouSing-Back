from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, login
from rest_framework import views
from rest_framework import status
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from django.conf import settings

from .models import *
from .serializers import *
import WhatDoYouSing
import requests
import allauth
from rest_framework import generics

#from rest_auth.registration.views import SocialLoginView                   
from allauth.socialaccount.providers.kakao import views as kakao_views     
from allauth.socialaccount.providers.oauth2.client import OAuth2Client  
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter

# Create your views here.

BASE_URL = 'http://whatdoyousing.com/'
#BASE_URL = 'http://127.0.0.1:8000/'

KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY":getattr(WhatDoYouSing.settings.base, 'KAKAO_CLIENT_ID', None),
    "KAKAO_REDIRECT_URI": f"http://whatdoyousing.com/accounts/kakao/callback/",
    "KAKAO_CLIENT_SECRET_KEY": getattr(WhatDoYouSing.settings.base, 'KAKAO_CLIENT_SECRET_KEY', None), 
    "KAKAO_PW":getattr(WhatDoYouSing.settings.base, 'KAKAO_PW', None),
}
kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

#자체 회원가입, 프로필 설정 포함
class SignUpView(views.APIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'회원가입 성공', 'data':serializer.data}, status=status.HTTP_200_OK)
        return Response({'message':'회원가입 실패', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
class ProfileChoiceView(views.APIView):
    serializer_class = ProfileChoiceSerializer
    
    def get(self, request, format=None):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def patch(self, request, format=None):
        serializer = ProfileChoiceSerializer(request.user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '프로필 변경 성공.', 'data': serializer.validated_data}, status=status.HTTP_200_OK)
        return Response({'message': '프로필 변경 실패.', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(views.APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response({'message': "로그인 성공", 'data': serializer.validated_data}, status=status.HTTP_200_OK)
        return Response({'message':'로그인 실패', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
class DuplicateIDView(views.APIView):
    def post(self, request):
        username = request.data.get('username')

        if User.objects.filter(username=username).exists():
            response_data = {'duplicate':True}
        else:
            response_data = {'duplicate':False}
        
        return Response(response_data, status=status.HTTP_200_OK)
    
class ChangePasswordView(views.APIView):
    serializer_class = PasswordUpdateSerializer

    def patch(self, request, format=None):
        serializer = PasswordUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

            # 현재 비밀번호 확인
            if not user.check_password(current_password):
                return Response({'message': '현재 비밀번호가 옳지 않습니다.'}, status=HTTP_400_BAD_REQUEST)

            # 새로운 비밀번호 설정
            user.set_password(new_password)
            user.save()

            return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '올바르지 않은 데이터입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        

class ChangeNicknameView(views.APIView):
    serializer_class = NicknameUpdateSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def patch(self, request, format=None):
        serializer = NicknameUpdateSerializer(request.user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '닉네임 변경 성공.', 'data': serializer.validated_data}, status=status.HTTP_200_OK)
        return Response({'message': '닉네임 변경 실패.', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(generics.DestroyAPIView):
    serializer_class = UserDeleteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        password = serializer.validated_data['password']

        if not user.check_password(password):
            return Response({'message': '접근 실패, 비밀번호가 옳지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()

        return Response({'message': '접근 성공. 회원 탈퇴가 완료되었습니다.'}, status=status.HTTP_200_OK)

'''
class UserAccessView(views.APIView):
    serializer_class=UserConfirmSerializer

    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            enter_password = serializer.validated_data['enter_password']

            if not user.check_password(enter_password):
                return Response({'message': '접근 실패, 비밀번호가 옳지 않습니다.', 'access':False}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': '접근 성공.', 'access':True}, status=status.HTTP_200_OK)
'''

class UserAccessView(generics.RetrieveAPIView):
    serializer_class = UserAccessSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        password = serializer.validated_data['password']

        if not user.check_password(password):
            return Response({'message': '접근 실패, 비밀번호가 옳지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # If the password is correct, return user information (You can customize this part)
        user_data = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'profile': user.profile,
        }

        return Response({'message': '접근 성공', 'data': user_data}, status=status.HTTP_200_OK)

#카카오
class KakaoLoginView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        client_id = KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = KAKAO_CONFIG['KAKAO_REDIRECT_URI']

        uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        
        res = redirect(uri)
        # res = requests.get(uri)
        print(res.get("access_tocken"))
        return res
    

class KakaoCallbackView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request):  
        data = request.query_params.copy()

        code = data.get('code')
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request_data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_CONFIG['KAKAO_REST_API_KEY'],
            'redirect_uri': KAKAO_CONFIG['KAKAO_REDIRECT_URI'],
            'client_secret': KAKAO_CONFIG['KAKAO_CLIENT_SECRET_KEY'],
            'code': code,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post(kakao_token_uri, data=request_data, headers=token_headers)

        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}" \

        # kakao 회원정보 요청
        auth_headers = {
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.get(kakao_profile_uri, headers=auth_headers)
        user_info_json = user_info_res.json()

        social_type = 'kakao'
        social_id = f"{social_type}_{user_info_json.get('id')}"

        properties = user_info_json.get('properties',{})
        nickname=properties.get('nickname','')
        profile=properties.get('thumbnail_image_url','')
        print(user_info_json)

        # 회원가입 및 로그인 처리 
        try:   
            user_in_db = User.objects.get(username=social_id) 
            # kakao계정 아이디가 이미 가입한거라면 
            # 서비스에 rest-auth 로그인
            data={'username':social_id,'password':social_id}
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                return Response({'message': "카카오 로그인 성공", 'data': serializer.validated_data}, status=status.HTTP_200_OK)
            return Response({'message': "카카오 로그인 실패", 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:   
            # 회원 정보 없으면 회원가입 후 로그인
            # def post(self,request):
            print("회원가입")
            data={'username':social_id,'password':social_id,'nickname':nickname,'profile':profile}
            serializer=KSignUpSerializer(data=data)  
            if serializer.is_valid():
                serializer.save()                          # 회원가입
                data1={'username':social_id,'password':social_id}
                serializer1 = LoginSerializer(data=data1)
                if serializer1.is_valid():
                    return Response({'message':'카카오 회원가입 성공','data':serializer1.validated_data}, status=status.HTTP_201_CREATED)
            return Response({'message':'카카오 회원가입 실패','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)