from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','nickname']

    def create(self, validated_data):

        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError('이미 사용 중인 아이디입니다.')

        user = User.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def update(self, validated_data):
        password = validated_data.get("password",None)

class ProfileChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id','profile']

    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username=data.get("username", None)
        password=data.get("password", None)

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise serializers.ValidationError('잘못된 비밀번호입니다.')
            else:
                token = RefreshToken.for_user(user)
                refresh = str(token)
                access = str(token.access_token)

                data = {
                    'id': user.id,
                    'username': user.username, #이거 없으면 KeyError 뜸
                    'nickname': user.nickname ,
                    'access_token': access
                }

                return data
        else: 
            raise serializers.ValidationError('존재하지 않는 사용자입니다.')
        
class UsernameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']
    
    #def validate_username(self, value):
    #    existing_user = User.objects.filter(nickname__iexact=value).first()
    #    if existing_user:
    #        raise serializers.ValidationError('이미 사용 중인 아이디입니다.')
    #    return value

class NicknameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','nickname']
    
    def validate_nickname(self, value):
        existing_user = User.objects.filter(nickname__iexact=value).first()
        if existing_user:
            raise serializers.ValidationError('이미 사용 중인 닉네임입니다.')
        return value

    
class PasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_new_password = serializers.CharField(max_length=128, write_only=True)

class UserConfirmSerializer(serializers.Serializer):
    enter_password = serializers.CharField(max_length=128, write_only=True)