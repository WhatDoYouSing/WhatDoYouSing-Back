from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, login
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from django.conf import settings

from .models import *
from .serializers import *

# Create your views here.

class SignUpView(views.APIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'회원가입 성공', 'data':serializer.data})
        return Response({'message':'회원가입 실패', 'error':serializer.errors})
    
class ProfileChoiceView(views.APIView):
    serializer_class = ProfileChoiceSerializer
    
    def get(self, request, format=None):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    
    def patch(self, request, format=None):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '프로필 지정 성공.', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': '프로필 지정 실패.', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    
class LoginView(views.APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response({'message':'로그인 성공', 'data':serializer.data})
        return Response({'message':'로그인 실패', 'error':serializer.errors})
    
class DuplicateIDView(views.APIView):
    def post(self, request):
        username = request.data.get('username')

        if User.objects.filter(username=username).exists():
            response_data = {'duplicate':True}
        else:
            response_data = {'duplicate':False}
        
        return Response(response_data, status=HTTP_200_OK)
    
class ChangeUsernameView(views.APIView):
    serializer_class = UsernameUpdateSerializer
    
    def get(self, request, format=None):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UsernameUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            new_username = serializer.validated_data['new_username']

            # 새로운 아이디 설정
            user.set_username(new_username)
            user.save()

            return Response({'message': '아이디 변경 성공.'}, status=HTTP_200_OK)
        else:
            return Response({'message': '올바르지 않은 데이터입니다.'}, status=HTTP_400_BAD_REQUEST)

    
class ChangePasswordView(views.APIView):
    serializer_class = PasswordUpdateSerializer
    def post(self, request, format=None):
        serializer = PasswordUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']
            confirm_new_password = serializer.validated_data['confirm_new_password']

            # 새로운 비밀번호 확인
            if new_password != confirm_new_password:
                return Response({'message': '새로운 비밀번호와 확인 비밀번호가 일치하지 않습니다.'}, status=HTTP_400_BAD_REQUEST)

            # 새로운 비밀번호 설정
            user.set_password(new_password)
            user.save()

            return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'}, status=HTTP_200_OK)
        else:
            return Response({'message': '올바르지 않은 데이터입니다.'}, status=HTTP_400_BAD_REQUEST)
        
        
class ChangeNicknameView(views.APIView):
    serializer_class = NicknameUpdateSerializer
    
    def get(self, request, format=None):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    
    def patch(self, request, format=None):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '닉네임 변경 성공.', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': '닉네임 변경 실패.', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

class UserDeleteView(views.APIView):
    serializer_class=UserConfirmSerializer
    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            enter_password = serializer.validated_data['enter_password']

            if not user.check_password(enter_password):
                return Response({'message': '접근 실패, 비밀번호가 옳지 않습니다.', 'access':False}, status=HTTP_400_BAD_REQUEST)
            else:
                #user = request.user
                user.delete()
                return Response({'message': '접근 성공. 회원 탈퇴가 완료되었습니다.', 'access':True}, status=HTTP_200_OK)
    
class UserAccessView(views.APIView):
    serializer_class=UserConfirmSerializer
    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            enter_password = serializer.validated_data['enter_password']

            if not user.check_password(enter_password):
                return Response({'message': '접근 실패, 비밀번호가 옳지 않습니다.', 'access':False}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': '접근 성공.', 'access':True}, status=HTTP_200_OK)